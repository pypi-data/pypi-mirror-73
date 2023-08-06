from PySide2 import QtCore, QtWidgets

from .signal_qwidget import SignalQWidget


class SignalQCheckBox(SignalQWidget[QtWidgets.QCheckBox]):
    """Signal widget for qt QCheckbox."""

    set_text_signal = QtCore.Signal(str)
    set_checked_signal = QtCore.Signal(bool)

    def set_text(self, text: str) -> None:
        """Emits set_text_signal which sets text to widget.
        
        :param text: text which will be setted.
        """

        self.set_text_signal.emit(text)

    def set_checked(self, checked: bool) -> None:
        """Emits set_checked_signal which sets checked status for widget.
        
        :param checked: checked status which will be setted.
        """

        self.set_checked_signal.emit(checked)

    def _connect_extended_signals(self) -> None:
        self._connect_set_text_signal()
        self._connect_set_checked_signal()

    def _connect_set_text_signal(self) -> None:
        """Connects set_text_signal with set_text."""

        widget = self.widget

        @QtCore.Slot(str)  # type: ignore
        def set_text(text: str) -> None:
            """Sets text to widget.
            
            :param text: text which will be setted.
            """

            widget.setText(text)
        self.set_text_signal.connect(set_text)

    def _connect_set_checked_signal(self) -> None:
        """Connects set_checked_signal with set_checked."""

        widget = self.widget

        @QtCore.Slot(bool)  # type: ignore
        def set_checked(checked: bool) -> None:
            """Sets checked status for widget.
            
            :param checked: checked status which will be setted.
            """

            widget.setChecked(checked)
        self.set_checked_signal.connect(set_checked)
