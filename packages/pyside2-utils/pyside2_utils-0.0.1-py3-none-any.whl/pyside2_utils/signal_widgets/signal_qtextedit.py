from PySide2 import QtCore, QtWidgets, QtGui

from .signal_qwidget import SignalQWidget


class SignalQTextEdit(SignalQWidget[QtWidgets.QTextEdit]):
    """Signal widget for Qt QTextEdit."""

    set_text_signal = QtCore.Signal(str)
    append_text_signal = QtCore.Signal(str)
    set_text_color_signal = QtCore.Signal(QtGui.QColor)

    def set_text(self, text: str) -> None:
        """Emits set_text_signal which sets text to widget.
        
        :param text: text which will be setted.
        """

        self.set_text_signal.emit(text)

    def append_text(self, text: str) -> None:
        """Emits append_text_signal which appends text to widget.
        
        :param text: text which will be appended.
        """

        self.append_text_signal.emit(text)

    def set_text_color(self, color: QtGui.QColor) -> None:
        """Emits set_text_color_signal which sets text color to widget.
        
        :param color: color which will be setted.
        """

        self.set_text_color_signal.emit(color)

    def _connect_extended_signals(self) -> None:
        self._connect_set_text_signal()
        self._connect_append_text_signal()
        self._connect_set_text_color_signal()

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

    def _connect_append_text_signal(self) -> None:
        """Connects append_text_signal with append_text."""

        widget = self.widget

        @QtCore.Slot(str)  # type: ignore
        def append_text(text: str) -> None:
            """Appends text to widget.
            
            :param text: text which will be appended.
            """

            widget.append(text)
        self.append_text_signal.connect(append_text)

    def _connect_set_text_color_signal(self) -> None:
        """Connects set_text_color_signal with set_text_color."""

        widget = self.widget

        @QtCore.Slot(QtGui.QColor)  # type: ignore
        def set_text_color(color: QtGui.QColor) -> None:
            """Sets text color to widget.
            
            :param color: color which will be setted.
            """

            widget.setTextColor(color)

        self.set_text_color_signal.connect(set_text_color)
