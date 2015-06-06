#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QSize

class Gui (QtGui.QWidget):

    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()

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

        layout = QtGui.QVBoxLayout()

        chooseImageBtn = QtGui.QPushButton('Choose')
        loadDatabaseBtn = QtGui.QPushButton('Load DB')
        loadMetricBtn = QtGui.QComboBox()

        chooseImageBtn.clicked.connect(self.chooseQueryImg)

        layout.addWidget(chooseImageBtn)
        layout.addWidget(loadDatabaseBtn)
        layout.addWidget(loadMetricBtn)


        return layout

    def initVisualLayout(self):

        # widget = QtGui.QWidget()
        # scroll = QtGui.QScrollArea()
        # scroll.setWidget(widget)
        layout = QtGui.QGridLayout() # original + results
#        widget.setLayout(layout)


        # Display the images:
        self.queryImg = thumbnail('avatar.jpeg')
        
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

    def chooseQueryImg(self):

        currDir='.'
        
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', currDir)
        self.queryImg.setIcon(QtGui.QIcon(fname))



def thumbnail(resName, width=50, height=50):
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

# JUNK
def thumbnail2(resName, width=50, height=50):
    """
    Take the path to the image and, optionaly the wanted size and
    return the thumbnail of the image.

    """

    icon = QtGui.QPixmap(resName)
    btn  = QtGui.QLabel()
    btn.setPixmap(icon)
#    btn.setPixmapSize(QSize(width,heigh
    btn.setMaximumSize(width,height)
    btn.resize(width, height)

    return btn
    
