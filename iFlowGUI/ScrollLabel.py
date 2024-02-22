"""
File: ScrollLabel.py
Author: Andrea Bertagnoli
Date: 01/10/2024
Description: Brief description of the purpose of the file
"""

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class ScrollLabel(QScrollArea):
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        # making widget resizable
        self.setWidgetResizable(True)
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
        # vertical box layout
        lay = QVBoxLayout(content)
        # creating label
        self.label = QLabel(content)
        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # making label multi-line
        self.label.setWordWrap(True)
        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        """
        The function sets the text of a label.
        
        :param text: The text parameter is a string that represents the text that
        you want to set for the label
        """
        # setting text to the label
        self.label.setText(text)