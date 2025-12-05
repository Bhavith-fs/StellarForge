"""
Error logging and diagnostics module for StellarForge.
Provides centralized error tracking, logging, and recovery mechanisms.
"""

import logging
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
import traceback

from .exceptions import StellarForgeException


class ErrorSeverity(Enum):
    """Error severity levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"


@dataclass
class ErrorRecord:
    """Structured error record for tracking and analysis."""
    timestamp: str
    severity: str
    error_type: str
    error_code: str
    message: str
    context: Dict[str, Any]
    traceback: str
    component: str
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class ErrorLogger:
    """
    Centralized error logging system.
    Tracks errors, provides diagnostics, and logs to file.
    """
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(ErrorLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize error logger."""
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.errors: List[ErrorRecord] = []
        self.max_errors = 1000  # Keep last 1000 errors
        self.log_file: Optional[Path] = None
        self.error_callbacks: List[Callable] = []
        self.session_id: Optional[str] = None
        
        # Setup Python logging
        self.python_logger = logging.getLogger("StellarForge")
        self.python_logger.setLevel(logging.DEBUG)
        
        # Create logs directory
        self.logs_dir = Path.cwd() / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Setup file handler
        self._setup_file_handler()
        
        # Setup console handler
        self._setup_console_handler()
    
    def _setup_file_handler(self):
        """Setup file logging handler."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.logs_dir / f"stellarforge_{timestamp}.log"
        
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.python_logger.addHandler(file_handler)
    
    def _setup_console_handler(self):
        """Setup console logging handler."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.python_logger.addHandler(console_handler)
    
    def set_session_id(self, session_id: str):
        """Set session ID for tracking related errors."""
        self.session_id = session_id
    
    def log_exception(self, exception: Exception, component: str = "UNKNOWN",
                     severity: ErrorSeverity = ErrorSeverity.ERROR,
                     context: Optional[Dict[str, Any]] = None):
        """
        Log an exception with full context.
        
        Args:
            exception: The exception to log
            component: Component where error occurred
            severity: Error severity level
            context: Additional context information
        """
        # Extract error information
        if isinstance(exception, StellarForgeException):
            error_type = exception.__class__.__name__
            error_code = exception.error_code
            message = exception.message
            exc_context = {**exception.context, **(context or {})}
            tb = exception.traceback_str
        else:
            error_type = exception.__class__.__name__
            error_code = "UNKNOWN"
            message = str(exception)
            exc_context = context or {}
            tb = traceback.format_exc()
        
        # Create error record
        record = ErrorRecord(
            timestamp=datetime.now().isoformat(),
            severity=severity.value,
            error_type=error_type,
            error_code=error_code,
            message=message,
            context=exc_context,
            traceback=tb,
            component=component,
            session_id=self.session_id
        )
        
        # Store error record
        self.errors.append(record)
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)
        
        # Log to Python logger
        log_method = getattr(self.python_logger, severity.value.lower(), 
                           self.python_logger.error)
        log_method(f"[{component}] {error_code}: {message}")
        
        # Call registered callbacks
        for callback in self.error_callbacks:
            try:
                callback(record)
            except Exception as cb_error:
                self.python_logger.error(f"Error in callback: {cb_error}")
    
    def log_error(self, message: str, component: str = "UNKNOWN",
                 severity: ErrorSeverity = ErrorSeverity.ERROR,
                 context: Optional[Dict[str, Any]] = None,
                 error_code: str = "GENERAL_ERROR"):
        """
        Log an error message.
        
        Args:
            message: Error message
            component: Component where error occurred
            severity: Error severity level
            context: Additional context
            error_code: Error code for tracking
        """
        record = ErrorRecord(
            timestamp=datetime.now().isoformat(),
            severity=severity.value,
            error_type="GeneralError",
            error_code=error_code,
            message=message,
            context=context or {},
            traceback="",
            component=component,
            session_id=self.session_id
        )
        
        self.errors.append(record)
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)
        
        log_method = getattr(self.python_logger, severity.value.lower(),
                           self.python_logger.error)
        log_method(f"[{component}] {error_code}: {message}")
        
        for callback in self.error_callbacks:
            try:
                callback(record)
            except Exception as cb_error:
                self.python_logger.error(f"Error in callback: {cb_error}")
    
    def register_error_callback(self, callback: Callable[[ErrorRecord], None]):
        """
        Register a callback to be called when errors occur.
        
        Args:
            callback: Callable that receives ErrorRecord
        """
        self.error_callbacks.append(callback)
    
    def get_errors(self, component: Optional[str] = None,
                  severity: Optional[ErrorSeverity] = None,
                  limit: int = 100) -> List[ErrorRecord]:
        """
        Get logged errors with optional filtering.
        
        Args:
            component: Filter by component
            severity: Filter by severity level
            limit: Maximum number of errors to return
            
        Returns:
            List of error records
        """
        filtered = self.errors
        
        if component:
            filtered = [e for e in filtered if e.component == component]
        
        if severity:
            filtered = [e for e in filtered if e.severity == severity.value]
        
        return filtered[-limit:]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of logged errors."""
        return {
            'total_errors': len(self.errors),
            'by_severity': self._count_by_severity(),
            'by_component': self._count_by_component(),
            'by_error_code': self._count_by_error_code(),
            'latest_error': self.errors[-1].to_dict() if self.errors else None
        }
    
    def _count_by_severity(self) -> Dict[str, int]:
        """Count errors by severity."""
        counts = {}
        for error in self.errors:
            counts[error.severity] = counts.get(error.severity, 0) + 1
        return counts
    
    def _count_by_component(self) -> Dict[str, int]:
        """Count errors by component."""
        counts = {}
        for error in self.errors:
            counts[error.component] = counts.get(error.component, 0) + 1
        return counts
    
    def _count_by_error_code(self) -> Dict[str, int]:
        """Count errors by error code."""
        counts = {}
        for error in self.errors:
            counts[error.error_code] = counts.get(error.error_code, 0) + 1
        return counts
    
    def export_errors(self, filepath: Path) -> bool:
        """
        Export error logs to JSON file.
        
        Args:
            filepath: Path to export to
            
        Returns:
            True if successful
        """
        try:
            export_data = {
                'session_id': self.session_id,
                'export_timestamp': datetime.now().isoformat(),
                'total_errors': len(self.errors),
                'errors': [e.to_dict() for e in self.errors],
                'summary': self.get_error_summary()
            }
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.python_logger.info(f"Errors exported to {filepath}")
            return True
        except Exception as e:
            self.python_logger.error(f"Failed to export errors: {e}")
            return False
    
    def clear_errors(self):
        """Clear all logged errors."""
        self.errors.clear()
        self.python_logger.info("Error log cleared")
    
    def get_log_file(self) -> Optional[Path]:
        """Get path to current log file."""
        return self.log_file


# Global error logger instance
_error_logger = ErrorLogger()


def get_error_logger() -> ErrorLogger:
    """Get the global error logger instance."""
    return _error_logger
