#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QSize

class Gui (QtGui.QWidget):

    def __init__(self):
        super(Gui, self).__init__()
        self.initConfiguration()
        self.initUI()

    def initConfiguration():
        """ This method declares/defines programs configuration variables."""
        self.currDir = '.'
        self.DB = None

    def initUI(self):

        mainLayout = QtGui.QHBoxLayout()
       
        configsLayout = self.initConfigsLayout()
        visualLayout = self.initVisualLayout()

        resultsLayout = QtGui.QGridLayout()
        # addStretch ?

        mainLayout.addLayout(configsLayout)
        mainLayout.addLayout(visualLayout)

        self.setLayout(mainLayout)
        
        self.setGeometry(300, 200, 640, 480)
        self.setWindowTitle('CBIREAVER')    
        self.show()

    def initConfigsLayout(self):
        """ Configs layout contains users options:
        image to query
        database to match upon
        similarity metric
        """

        def populateMetrics():
            loadMetricBtn.addItem('L1')
            loadMetricBtn.addItem('L2')

        layout = QtGui.QGridLayout()
        spacing = 10
        layout.setSpacing(spacing)

        # Buttons
        executeQueryBtn = QtGui.QPushButton('Execute query')
        chooseImageBtn = QtGui.QPushButton('Query image')
        loadDatabaseBtn = QtGui.QPushButton('Load DB')
        loadMetricBtn = QtGui.QComboBox()
        numberOfImagesSB = QtGui.QSpinBox()
        populateMetrics ()

        # Labels
        chooseImageLbl = QtGui.QLabel('Image not choosen')
        loadDatabaseLbl = QtGui.QLabel('Database not loaded')
        loadMetricLbl = QtGui.QLabel()

        # Adjust the button dimensions
        width  = 100
        height = 30
        chooseImageBtn.setMaximumSize(width,height)
        loadDatabaseBtn.setMaximumSize(width,height)
        loadMetricBtn.setMaximumSize(width,height)
        numberOfImagesSB.setMaximumSize(width,height)        

        chooseImageBtn.clicked.connect(lambda: self.chooseQueryImg(chooseImageLbl))
        loadDatabaseBtn.clicked.connect(lambda: self.chooseDB(loadDatabaseLbl))

        layout.addWidget(chooseImageBtn, 0, 1)
        layout.addWidget(loadDatabaseBtn, 1, 1)
        layout.addWidget(loadMetricBtn, 2, 1, 2 ,1)
        layout.addWidget(numberOfImagesSB, 3, 1)
        layout.addWidget(executeQueryBtn, 4, 1, 3, 1)


        layout.addWidget(chooseImageLbl, 0, 2)
        layout.addWidget(loadDatabaseLbl, 1, 2)
        layout.addWidget(loadMetricLbl, 2, 2)

        return layout

    def initVisualLayout(self):

        # widget = QtGui.QWidget()
        # scroll = QtGui.QScrollArea()
        # scroll.setWidget(widget)
        layout = QtGui.QGridLayout() # original + results
#        widget.setLayout(layout)


        # Display the images:
        self.queryImg = thumbnail('linux-python-logo.jpg')
        
        layout.addWidget(self.queryImg, 0, 2)
        self.populateResultGrid(layout)

        return layout

    def populateResultGrid(self, grid):

        cnt = 20
        ncol = 5

        r = 1
        c = 0

        for n in range(0, cnt):

            path = 'images/' + str(n) + '.jpg'
            if n % ncol == 0:
                r = r + 1
                c = 0

            thumb = thumbnail(path)
            grid.addWidget(thumb, r, c)

            c = c+1

        return

    def chooseQueryImg(self, label):
        """ Choose the query image."""
        
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.currDir)
        self.queryImg.setIcon(QtGui.QIcon(fname))
        label.setText(fname)

    def chooseDB (self, label):
        """ Choose the image database."""
        
        db_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.currDir)
        label.setText(db_name)
        self


def thumbnail(resName, width=70, height=70):
    """
    Take the path to the image and, optionaly the wanted size and
    return the thumbnail of the image.

    """

    icon = QtGui.QIcon(resName)
    btn  = QtGui.QPushButton()
    btn.setIcon(icon)
    btn.setIconSize(QSize(width,height))
    btn.resize(width,height)
    btn.setMaximumSize(width,height)
    btn.setMinimumSize(width,height)

    return btn


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    

"""
TODO
thumbnail borders
scrollable grid
"""
    
