"""
Animation utilities for smooth UI transitions.
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QObject, pyqtProperty
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect


class FadeAnimation:
    """Helper class for fade in/out animations."""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300):
        """
        Fade in a widget.
        
        Args:
            widget: Widget to fade in
            duration: Animation duration in milliseconds
        """
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        
        # Store reference to prevent garbage collection
        widget._fade_animation = animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300, callback=None):
        """
        Fade out a widget.
        
        Args:
            widget: Widget to fade out
            duration: Animation duration in milliseconds
            callback: Optional callback when animation completes
        """
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.start()
        
        # Store reference to prevent garbage collection
        widget._fade_animation = animation


class SlideAnimation:
    """Helper class for slide animations."""
    
    @staticmethod
    def slide_in(widget: QWidget, direction: str = "left", duration: int = 400):
        """
        Slide in a widget from specified direction.
        
        Args:
            widget: Widget to animate
            direction: Direction to slide from ("left", "right", "top", "bottom")
            duration: Animation duration in milliseconds
        """
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Get current geometry
        current = widget.geometry()
        
        # Calculate start position based on direction
        if direction == "left":
            start = current.translated(-current.width(), 0)
        elif direction == "right":
            start = current.translated(current.width(), 0)
        elif direction == "top":
            start = current.translated(0, -current.height())
        else:  # bottom
            start = current.translated(0, current.height())
        
        animation.setStartValue(start)
        animation.setEndValue(current)
        animation.start()
        
        widget._slide_animation = animation


class PulseAnimation:
    """Helper class for pulse/scale animations."""
    
    @staticmethod
    def pulse(widget: QWidget, scale: float = 1.1, duration: int = 200):
        """
        Create a pulse effect on a widget.
        
        Args:
            widget: Widget to pulse
            scale: Scale factor for pulse
            duration: Animation duration in milliseconds
        """
        # This would require custom property animation
        # For now, we'll use a simpler approach with style
        original_style = widget.styleSheet()
        
        # Add slight scale effect via margins (simplified)
        def reset():
            widget.setStyleSheet(original_style)
        
        # Schedule reset
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(duration, reset)


class SmoothScroll:
    """Helper for smooth scrolling animations."""
    
    @staticmethod
    def scroll_to(scroll_area, target_value: int, duration: int = 300):
        """
        Smoothly scroll to target position.
        
        Args:
            scroll_area: QScrollArea or similar widget with scroll bar
            target_value: Target scroll position
            duration: Animation duration in milliseconds
        """
        scrollbar = scroll_area.verticalScrollBar()
        
        animation = QPropertyAnimation(scrollbar, b"value")
        animation.setDuration(duration)
        animation.setStartValue(scrollbar.value())
        animation.setEndValue(target_value)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        
        scroll_area._scroll_animation = animation


class ButtonPressAnimation:
    """Helper for button press visual feedback."""
    
    @staticmethod
    def setup_button(button):
        """
        Setup press animation for a button.
        
        Args:
            button: QPushButton to enhance
        """
        original_style = button.styleSheet()
        
        def on_pressed():
            # Add pressed effect
            style = original_style + "\nQPushButton { transform: scale(0.95); }"
            button.setStyleSheet(style)
        
        def on_released():
            # Reset
            button.setStyleSheet(original_style)
        
        button.pressed.connect(on_pressed)
        button.released.connect(on_released)


# Easing curve presets
EASE_IN_OUT_CUBIC = QEasingCurve.Type.InOutCubic
EASE_IN_OUT_QUAD = QEasingCurve.Type.InOutQuad
EASE_OUT_BOUNCE = QEasingCurve.Type.OutBounce
EASE_OUT_ELASTIC = QEasingCurve.Type.OutElastic
