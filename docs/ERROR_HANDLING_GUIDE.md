# Error Handling & Diagnostics Guide for StellarForge

## Overview

StellarForge now includes a comprehensive error handling and diagnostics system to track, analyze, and recover from application crashes and errors. This document explains the error handling architecture and how to use it.

## Components

### 1. Custom Exceptions (`src/core/exceptions.py`)

**Purpose**: Structured exception hierarchy for specific error types.

**Available Exception Classes**:

- `StellarForgeException`: Base exception with structured context
- `EngineInitializationError`: Engine startup failures
- `SimulationError`: Physics simulation issues
- `RenderingError`: 3D visualization problems
- `UIError`: User interface failures
- `DataValidationError`: Invalid data detected
- `ConfigurationError`: Configuration issues
- `MemoryError`: Memory allocation failures
- `FileOperationError`: File I/O issues

**Usage Example**:
```python
from core.exceptions import EngineInitializationError

try:
    engine.initialize(particle_count)
except EngineInitializationError as e:
    print(f"Error Code: {e.error_code}")
    print(f"Details: {e.context}")
    print(f"Traceback: {e.traceback_str}")
```

### 2. Error Logger (`src/core/error_logger.py`)

**Purpose**: Centralized logging and error tracking with multiple output channels.

**Key Features**:
- Structured error recording with context
- File-based logging
- Console output
- Error callbacks for UI integration
- Error statistics and analysis
- JSON export capabilities

**Usage Examples**:

```python
from core.error_logger import get_error_logger, ErrorSeverity

error_logger = get_error_logger()

# Log an exception
try:
    some_operation()
except Exception as e:
    error_logger.log_exception(
        e,
        component="MODULE_NAME",
        severity=ErrorSeverity.ERROR,
        context={'additional_info': 'value'}
    )

# Log a simple error message
error_logger.log_error(
    "Something went wrong",
    component="MODULE_NAME",
    severity=ErrorSeverity.WARNING,
    error_code="CUSTOM_ERROR_CODE"
)

# Get error summary
summary = error_logger.get_error_summary()
print(f"Total Errors: {summary['total_errors']}")

# Export logs
error_logger.export_errors(Path("logs/errors.json"))
```

### 3. Error Diagnostics (`src/core/error_diagnostics.py`)

**Purpose**: Generate diagnostic reports and recovery strategies.

**Classes**:

#### SystemDiagnostics
Collects system information:
- Platform and Python version
- Memory usage and availability
- CPU information
- Process-specific stats

```python
from core.error_diagnostics import SystemDiagnostics

diagnostics = SystemDiagnostics.get_full_diagnostics()
print(f"Available Memory: {diagnostics['memory']['available_memory_mb']} MB")
print(f"CPU Usage: {diagnostics['cpu']['cpu_percent']}%")
```

#### ErrorDiagnosticReport
Generates comprehensive diagnostic reports:

```python
from core.error_diagnostics import ErrorDiagnosticReport
from pathlib import Path

report_gen = ErrorDiagnosticReport()
report = report_gen.generate_report(Path("logs/diagnostic.json"))
```

#### ErrorRecoveryStrategy
Provides recovery suggestions:

```python
from core.error_diagnostics import ErrorRecoveryStrategy

suggestion = ErrorRecoveryStrategy.get_recovery_suggestion(exception)
print(suggestion)
```

#### ErrorContextManager
Context manager for operation tracking:

```python
from core.error_diagnostics import ErrorContextManager

with ErrorContextManager("load_data", "DATA_LOADER"):
    load_data_from_file()
```

## Error Handling in Application

### Main Entry Point (`main.py`)

The main.py file now includes:
- Global error handler setup
- Session ID tracking
- Uncaught exception handler
- Error dialog display
- Log export on exit

### MainWindow (`src/gui/main_window.py`)

Error handling added to:
- `__init__()`: Constructor with initialization error handling
- `init_ui()`: UI initialization with per-component error handling
- `init_engine()`: Engine setup with validation
- `update_simulation()`: Simulation loop with recovery
- All event handlers

**Key Pattern**:
```python
try:
    # Operation
    result = operation()
except SpecificError:
    # Handle specific error
    raise
except Exception as e:
    # Log and re-raise
    self.error_logger.log_exception(e, "COMPONENT")
    raise CustomError(..., cause=e)
```

### UniverseRenderer (`src/vis/universe_renderer.py`)

Error handling for:
- Canvas/view creation
- Camera setup
- Markers visual creation
- Particle data updates
- Data validation

### MockEngine (`src/engine_bridge/mock_engine.py`)

Error handling for:
- Engine initialization
- Position generation
- Velocity calculation
- Simulation steps
- Data validation

## Error Log Files

### Log Locations

- **Main Log**: `logs/stellarforge_YYYYMMDD_HHMMSS.log`
- **Error Export**: `logs/final_error_report.json`
- **Diagnostics**: `logs/diagnostic_report.json`
- **Crash Reports**: `logs/crash_report.json`

### Log Format

Each error record contains:
```json
{
  "timestamp": "2025-12-05T10:30:45.123456",
  "severity": "ERROR",
  "error_type": "SimulationError",
  "error_code": "SIMULATION_ERROR",
  "message": "Simulation step failed",
  "context": {
    "dt": 0.016,
    "particle_count": 1000
  },
  "traceback": "...",
  "component": "SIMULATION_UPDATE",
  "session_id": "uuid-string"
}
```

## Severity Levels

- **DEBUG**: Development-level information
- **INFO**: General information
- **WARNING**: Warning that doesn't prevent operation
- **ERROR**: Error that affects functionality
- **CRITICAL**: Critical error affecting major features
- **FATAL**: Application-level failure

## Best Practices

### 1. Always Wrap Risky Operations
```python
try:
    risky_operation()
except SpecificException as e:
    error_logger.log_exception(
        e,
        component="MY_COMPONENT",
        severity=ErrorSeverity.ERROR
    )
    # Handle gracefully or re-raise
```

### 2. Provide Context
```python
error_logger.log_exception(
    e,
    component="PROCESSOR",
    context={
        'file_path': str(file),
        'particle_count': 1000,
        'attempt': 3
    }
)
```

### 3. Use Error Codes for Tracking
```python
error_logger.log_error(
    "Network timeout",
    component="NETWORK",
    error_code="NETWORK_TIMEOUT_60S"
)
```

### 4. Don't Suppress Errors
Instead of `except: pass`, log them:
```python
try:
    operation()
except Exception as e:
    error_logger.log_exception(
        e,
        component="CLEANUP",
        severity=ErrorSeverity.WARNING
    )
```

### 5. Use Context Managers for Operations
```python
with ErrorContextManager("particle_update", "RENDERER"):
    update_particles()
```

## Troubleshooting

### Application Crashes

1. **Check the log files** in `logs/` directory
2. **Review error summary**: Look for error code patterns
3. **Generate diagnostics**: Use `ErrorDiagnosticReport`
4. **Check system resources**: Memory, CPU usage

### Specific Error Codes

- **ENGINE_INIT_ERROR**: Engine failed to initialize
  - Solution: Reduce particle count, check memory
  
- **RENDERING_ERROR**: 3D rendering failed
  - Solution: Update GPU drivers, reduce particle count
  
- **SIMULATION_ERROR**: Physics step failed
  - Solution: Check for invalid data, restart simulation
  
- **DATA_VALIDATION_ERROR**: Invalid data
  - Solution: Reload from file, clear cache

## Integration with UI

Error handling is integrated with the UI to:
1. Display error dialogs for critical errors
2. Pause simulation on errors
3. Update status bar with error status
4. Log all errors with full context

## Performance Monitoring

The error logger also tracks performance:
- FPS monitoring
- Frame time tracking
- Operation duration
- Memory usage

Access via:
```python
summary = error_logger.get_error_summary()
print(summary['by_severity'])
print(summary['by_component'])
```

## Future Improvements

Potential enhancements:
1. Real-time error dashboard
2. Automatic error recovery strategies
3. Performance profiling
4. Remote error reporting
5. User feedback system
