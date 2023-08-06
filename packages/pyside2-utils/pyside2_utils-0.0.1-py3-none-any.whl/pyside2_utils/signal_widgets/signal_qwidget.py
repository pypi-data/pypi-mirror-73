import sys

from typing import Generic

from PySide2 import QtCore, QtWidgets

from .types import WidgetType
from .signal_qobject import SignalQObject


class SignalQWidget(SignalQObject, Generic[WidgetType]):
    """This class is builder for another signal widgets.
    This class is wrap over qt widget, in which
    are connected signals for comfortable work with widget.
    """

    set_property_signal = QtCore.Signal(str, str)
    update_polish_signal = QtCore.Signal()
    set_property_and_update_polish_signal = QtCore.Signal(str, str)
    set_style_sheet_signal = QtCore.Signal(str)
    update_style_sheet_signal = QtCore.Signal()
    set_enabled_signal = QtCore.Signal(bool)
    set_visible_signal = QtCore.Signal(bool)

    def __init__(self, widget: WidgetType) -> None:
        """Initialize signal widget."""

        super().__init__()

        self.widget = widget
        self._connect_signals()

    def set_property(self, property_: str, value: str) -> None:
        """Emits set_property_signal which sets property for widget.

        :param property_: property which will be setted.
        :param value: value for property_.
        """

        self.set_property_signal.emit(property_, value)

    def update_polish(self) -> None:
        """Emits update_polish_signal which updates widget style polish."""

        self.update_polish_signal.emit()
    
    def set_property_and_update_polish(self, property_: str, value: str) -> None:
        """Emits set_property_and_update_polish_signal which 
        sets property for widget and then updates widget style polish.
        
        :param property_: property which will be setted.
        :param value: value for property_.
        """

        self.set_property_and_update_polish_signal.emit(property_, value)

    def set_style_sheet(self, style_sheet: str) -> None:
        """Emits set style sheet signal which sets style sheet for widget.
        
        :param style_sheet: style sheet which will be setted.
        """

        self.set_style_sheet_signal.emit(style_sheet)

    def update_style_sheet(self) -> None:
        """Emits update style sheet signal which updates style sheet for widget."""

        self.update_style_sheet_signal.emit()

    def set_enabled(self, enabled: bool) -> None:
        """Emits set enabled signal which sets widget enabled status.
        
        :param enabled: enabled status which will be setted.
        """

        self.set_enabled_signal.emit(enabled)

    def set_visible(self, visible: bool) -> None:
        """Emits set visible signal which sets widget visible status.
        
        :param visible: visible status which will be setted.
        """

        self.set_visible_signal.emit(visible)

    def _connect_signals(self) -> None:
        """Connects widget signals."""

        self._connect_set_property_signal()
        self._connect_update_polish_signal()
        self._connect_set_property_and_update_polish_signal()
        self._connect_set_style_sheet_signal()
        self._connect_update_style_sheet_signal()
        self._connect_set_enabled_signal()
        self._connect_set_visible_signal()

        self._connect_extended_signals()

    def _connect_extended_signals(self) -> None:
        """Connects signals which implemented in the heir.
        Can be optional implemented for the heir.
        """

    def _connect_set_property_signal(self) -> None:
        """Connects set_property_signal with set_property."""

        widget = self.widget

        @QtCore.Slot()  # type: ignore
        def set_property(property_: str, value: str) -> None:
            """Sets property for widget.
            
            :param property_: property which will be setted.
            :param value: value for property_.
            """

            widget.setProperty(property_, value)
        self.set_property_signal.connect(set_property)

    def _connect_update_polish_signal(self) -> None:
        """Connects update_polish_signal with update_polish."""

        widget = self.widget

        @QtCore.Slot()  # type: ignore
        def update_polish() -> None:
            """Updates widget style polish."""

            widget.style().unpolish(widget)
            widget.style().polish(widget)
        self.update_polish_signal.connect(update_polish)

    def _connect_set_property_and_update_polish_signal(self) -> None:
        """Connects set_property_and_update_polish_signal with set_property_and_update_polish."""

        @QtCore.Slot(str, str)  # type: ignore
        def set_property_and_update_polish(property_: str, value: str) -> None:
            """Sets property for widget and then update his style polish.
        
            :param property_: property which will be setted.
            :param value: value for property_.
            """

            self.set_property(property_, value)
            self.update_polish()
        self.set_property_and_update_polish_signal.connect(set_property_and_update_polish)

    def _connect_set_style_sheet_signal(self) -> None:
        """Connects set_style_sheet_signal with set_style_sheet."""

        widget = self.widget

        @QtCore.Slot(str)  # type: ignore
        def set_style_sheet(style_sheet: str) -> None:
            """Set style sheet for widget.
        
            :param style_sheet: style sheet which will be setted.
            """

            widget.setStyleSheet(style_sheet)
        self.set_style_sheet_signal.connect(set_style_sheet)

    def _connect_update_style_sheet_signal(self) -> None:
        """Connects update_style_sheet_signal with update_style_sheet."""

        widget = self.widget

        @QtCore.Slot()  # type: ignore
        def update_style_sheet() -> None:
            """Updates widget stylesheet."""

            widget.setStyleSheet(widget.styleSheet())
        self.update_style_sheet_signal.connect(update_style_sheet)

    def _connect_set_enabled_signal(self) -> None:
        """Connects set_enabled_signal with set_enabled."""

        widget = self.widget

        @QtCore.Slot(bool)  # type: ignore
        def set_enabled(enabled: bool) -> None:
            """Sets widget enabled status.
        
            :param enabled: enabled status which will be setted.
            """

            widget.setEnabled(enabled)
        self.set_enabled_signal.connect(set_enabled)

    def _connect_set_visible_signal(self) -> None:
        """Connects set_visible_signal with set_visible."""

        widget = self.widget

        @QtCore.Slot(bool)  # type: ignore
        def set_visible(visible: bool) -> None:
            """Sets widget visible status.
        
            :param visible: visible status which will be setted.
            """

            widget.setVisible(visible)
        self.set_visible_signal.connect(set_visible)
