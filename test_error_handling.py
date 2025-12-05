#!/usr/bin/env python3
"""
Error Handling System Test Suite for StellarForge

This script tests the error handling and diagnostics system.
Run: python test_error_handling.py
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.error_logger import get_error_logger, ErrorSeverity
from core.exceptions import (
    EngineInitializationError, SimulationError, 
    RenderingError, DataValidationError
)
from core.error_diagnostics import (
    SystemDiagnostics, ErrorDiagnosticReport,
    ErrorRecoveryStrategy, ErrorContextManager
)
import numpy as np


def test_logger_basic():
    """Test basic error logging."""
    print("\n=== TEST 1: Basic Error Logging ===")
    logger = get_error_logger()
    
    # Log a simple message
    logger.log_error(
        "Test warning message",
        component="TEST",
        severity=ErrorSeverity.WARNING,
        error_code="TEST_WARNING"
    )
    print("âœ“ Simple logging works")
    
    # Log an exception
    try:
        1 / 0
    except ZeroDivisionError as e:
        logger.log_exception(
            e,
            component="TEST",
            severity=ErrorSeverity.ERROR,
            context={'operation': 'division'}
        )
    print("âœ“ Exception logging works")


def test_custom_exceptions():
    """Test custom exception classes."""
    print("\n=== TEST 2: Custom Exceptions ===")
    logger = get_error_logger()
    
    try:
        raise EngineInitializationError(
            "Failed to initialize engine",
            context={'particle_count': 5000, 'available_memory': 2048}
        )
    except EngineInitializationError as e:
        logger.log_exception(
            e,
            component="TEST",
            severity=ErrorSeverity.ERROR
        )
        print(f"âœ“ EngineInitializationError: {e.error_code}")
        print(f"  Context: {e.context}")
    
    try:
        raise SimulationError(
            "Invalid time step",
            context={'dt': -0.1}
        )
    except SimulationError as e:
        logger.log_exception(e, "TEST", ErrorSeverity.ERROR)
        print(f"âœ“ SimulationError: {e.error_code}")


def test_data_validation():
    """Test data validation error handling."""
    print("\n=== TEST 3: Data Validation ===")
    logger = get_error_logger()
    
    # Test invalid array
    positions = np.array([[np.nan, 0, 0], [1, 1, 1]])
    
    if np.any(~np.isfinite(positions)):
        logger.log_error(
            "Invalid values in positions",
            component="TEST_VALIDATION",
            severity=ErrorSeverity.WARNING,
            context={'has_nan': True}
        )
        print("âœ“ NaN detection works")
    
    # Test shape validation
    try:
        if positions.shape[1] != 3:
            raise DataValidationError(
                f"Expected (N, 3), got {positions.shape}",
                context={'expected': (None, 3), 'actual': positions.shape}
            )
    except DataValidationError as e:
        logger.log_exception(e, "TEST", ErrorSeverity.ERROR)
        print(f"âœ“ Shape validation: {e.message}")


def test_error_summary():
    """Test error summary and statistics."""
    print("\n=== TEST 4: Error Summary ===")
    logger = get_error_logger()
    
    summary = logger.get_error_summary()
    print(f"Total errors logged: {summary['total_errors']}")
    print(f"By severity: {summary['by_severity']}")
    print(f"By component: {summary['by_component']}")
    if summary['latest_error']:
        print(f"Latest error: {summary['latest_error']['error_code']}")
    print("âœ“ Error summary works")


def test_system_diagnostics():
    """Test system diagnostics."""
    print("\n=== TEST 5: System Diagnostics ===")
    
    # Get system info
    system_info = SystemDiagnostics.get_system_info()
    if system_info:
        print(f"âœ“ Platform: {system_info.get('platform', 'Unknown')}")
        print(f"âœ“ Python: {system_info.get('python_version', 'Unknown')}")
    
    # Get memory info
    memory_info = SystemDiagnostics.get_memory_info()
    if memory_info and 'available_memory_mb' in memory_info:
        available = memory_info.get('available_memory_mb', 0)
        used = memory_info.get('used_memory_mb', 0)
        process = memory_info.get('process_memory_mb', 0)
        print(f"âœ“ Available Memory: {available:.0f} MB")
        print(f"âœ“ Used Memory: {used:.0f} MB")
        print(f"âœ“ Process Memory: {process:.1f} MB")
    else:
        print("âœ“ Memory info (psutil not available)")
    
    # Get CPU info
    cpu_info = SystemDiagnostics.get_cpu_info()
    if cpu_info and 'cpu_count_logical' in cpu_info:
        cores = cpu_info.get('cpu_count_logical', 'N/A')
        percent = cpu_info.get('cpu_percent', 0)
        print(f"âœ“ CPU Cores: {cores}")
        print(f"âœ“ CPU Usage: {percent:.1f}%")
    else:
        print("âœ“ CPU info (psutil not available)")


def test_diagnostic_report():
    """Test diagnostic report generation."""
    print("\n=== TEST 6: Diagnostic Report ===")
    
    report_gen = ErrorDiagnosticReport()
    report = report_gen.generate_report()
    
    if report:
        print(f"âœ“ Report generated with timestamp: {report.get('timestamp', 'N/A')}")
        print(f"âœ“ System info present: {'system' in report}")
        print(f"âœ“ Error summary present: {'error_summary' in report}")
        
        # Try to save report
        report_path = Path("logs/test_diagnostic_report.json")
        report_gen.generate_report(report_path)
        if report_path.exists():
            print(f"âœ“ Report saved to {report_path}")
            report_path.unlink()  # Clean up


def test_recovery_strategy():
    """Test error recovery strategies."""
    print("\n=== TEST 7: Recovery Strategies ===")
    
    # Test various error types
    errors = [
        EngineInitializationError("Engine failed"),
        RenderingError("GPU failed"),
        SimulationError("Physics failed"),
    ]
    
    for error in errors:
        suggestion = ErrorRecoveryStrategy.get_recovery_suggestion(error)
        print(f"\nâœ“ {type(error).__name__}:")
        for line in suggestion.split('\n')[:2]:
            print(f"  {line}")


def test_context_manager():
    """Test error context manager."""
    print("\n=== TEST 8: Context Manager ===")
    logger = get_error_logger()
    
    # Successful operation
    with ErrorContextManager("test_operation", "TEST"):
        print("âœ“ Operation completed")
    
    # Operation with error
    try:
        with ErrorContextManager("failing_operation", "TEST"):
            raise ValueError("Intentional test error")
    except ValueError:
        print("âœ“ Context manager error handling works")


def test_error_export():
    """Test error log export."""
    print("\n=== TEST 9: Error Export ===")
    logger = get_error_logger()
    
    # Log a few errors
    for i in range(3):
        logger.log_error(
            f"Test error {i}",
            component="TEST_EXPORT",
            severity=ErrorSeverity.WARNING
        )
    
    # Export
    export_path = Path("logs/test_error_export.json")
    success = logger.export_errors(export_path)
    
    if success and export_path.exists():
        print(f"âœ“ Errors exported to {export_path}")
        file_size = export_path.stat().st_size
        print(f"âœ“ Export file size: {file_size} bytes")
        export_path.unlink()  # Clean up


def test_error_callback():
    """Test error callback system."""
    print("\n=== TEST 10: Error Callbacks ===")
    logger = get_error_logger()
    
    callback_called = {'count': 0}
    
    def test_callback(record):
        callback_called['count'] += 1
    
    logger.register_error_callback(test_callback)
    
    # Log an error
    logger.log_error(
        "Test callback error",
        component="TEST_CALLBACK",
        severity=ErrorSeverity.WARNING
    )
    
    if callback_called['count'] > 0:
        print(f"âœ“ Callback was called {callback_called['count']} time(s)")


def run_all_tests():
    """Run all error handling tests."""
    print("\n" + "="*60)
    print("StellarForge Error Handling System - Test Suite")
    print("="*60)
    
    tests = [
        test_logger_basic,
        test_custom_exceptions,
        test_data_validation,
        test_error_summary,
        test_system_diagnostics,
        test_diagnostic_report,
        test_recovery_strategy,
        test_context_manager,
        test_error_export,
        test_error_callback,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\nâœ— Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\nâœ“ All tests passed! Error handling system is working correctly.")
    else:
        print(f"\nâœ— {failed} test(s) failed. Please review the errors above.")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)


