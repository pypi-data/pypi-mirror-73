from PySide2 import QtCore, QtWidgets

from .signal_qwidget import SignalQWidget


class SignalQLabel(SignalQWidget[QtWidgets.QLabel]):
    """Signal widget for qt QLabel."""

    set_text_signal = QtCore.Signal(str)

    def set_text(self, text: str) -> None:
        """Emits set_text_signal which sets text to widget.
        
        :param text: text which will be setted.
        """

        self.set_text_signal.emit(text)

    def _connect_extended_signals(self) -> None:
        self._connect_set_text_signal()

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
