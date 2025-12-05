"""
Custom exception classes for StellarForge application.
Provides detailed error hierarchy for better error tracking and debugging.
"""

import sys
import traceback
from typing import Optional, Dict, Any
from datetime import datetime


class StellarForgeException(Exception):
    """
    Base exception class for all StellarForge exceptions.
    Provides structured error information and context.
    """
    
    def __init__(self, message: str, error_code: str = "UNKNOWN", 
                 context: Optional[Dict[str, Any]] = None, 
                 cause: Optional[Exception] = None):
        """
        Initialize StellarForge exception.
        
        Args:
            message: Error message
            error_code: Unique error code for tracking
            context: Additional context information
            cause: Original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.cause = cause
        self.timestamp = datetime.now()
        self.traceback_str = traceback.format_exc()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging."""
        return {
            'error_type': self.__class__.__name__,
            'error_code': self.error_code,
            'message': self.message,
            'context': self.context,
            'timestamp': self.timestamp.isoformat(),
            'cause': str(self.cause) if self.cause else None,
            'traceback': self.traceback_str
        }
    
    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


class EngineInitializationError(StellarForgeException):
    """Raised when simulation engine fails to initialize."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="ENGINE_INIT_ERROR",
            context=context,
            cause=cause
        )


class SimulationError(StellarForgeException):
    """Raised when simulation step fails or produces invalid data."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="SIMULATION_ERROR",
            context=context,
            cause=cause
        )


class RenderingError(StellarForgeException):
    """Raised when 3D rendering fails."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="RENDERING_ERROR",
            context=context,
            cause=cause
        )


class UIError(StellarForgeException):
    """Raised when UI component fails."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="UI_ERROR",
            context=context,
            cause=cause
        )


class DataValidationError(StellarForgeException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="DATA_VALIDATION_ERROR",
            context=context,
            cause=cause
        )


class ConfigurationError(StellarForgeException):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="CONFIG_ERROR",
            context=context,
            cause=cause
        )


class MemoryError(StellarForgeException):
    """Raised when memory allocation or management fails."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="MEMORY_ERROR",
            context=context,
            cause=cause
        )


class FileOperationError(StellarForgeException):
    """Raised when file operations fail."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="FILE_ERROR",
            context=context,
            cause=cause
        )
