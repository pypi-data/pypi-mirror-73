from PySide2 import QtCore, QtWidgets

from .signal_qwidget import SignalQWidget


class SignalQMainWindow(SignalQWidget[QtWidgets.QMainWindow]):
    """Signal widget for qt QMainWindow."""
