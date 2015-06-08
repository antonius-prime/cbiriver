#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pickle
import imagesearch, metrics
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSize

class Gui (QtGui.QWidget):

    def __init__(self):
        """ Contructor delegates initialization to the helper methods. """
        
        super(Gui, self).__init__()
        self.initConfiguration()
        self.initUI()

    def initConfiguration(self):
        """ This method declares/defines programs configuration variables."""

        self.currDir = '.'
        self.searcher = None
        self.vocabulary = None
        self.DB = None
        self.metric = None
        self.metricDict = {}
        self.nbr_images = 5
        self.imgName = None

        with open('vocabulary.pkl', 'rb') as f:
            self.voc = pickle.load(f)

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
            l1 = 'L1'
            l2 = 'L2'
            self.metricDict[l1] = metrics.L1
            self.metricDict[l2] = metrics.L2            
            loadMetricBtn.addItem(l1)
            loadMetricBtn.addItem(l2)

        layout = QtGui.QGridLayout()
        spacing = 10
        layout.setSpacing(spacing)

        # Buttons
        executeQueryBtn = QtGui.QPushButton('Execute query')
        chooseImageBtn = QtGui.QPushButton('Query image')
        loadDatabaseBtn = QtGui.QPushButton('Load DB')
        loadMetricBtn = QtGui.QComboBox()
        numberOfImagesSB = QtGui.QSpinBox()
        numberOfImagesSB.setValue(self.nbr_images)
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

        # signals
        chooseImageBtn.clicked.connect(lambda: self.chooseQueryImg(chooseImageLbl))
        loadDatabaseBtn.clicked.connect(lambda: self.chooseDB(loadDatabaseLbl))
        self.connect(loadMetricBtn, QtCore.SIGNAL('activated(QString)'), self.chooseMetric)
        self.connect(executeQueryBtn, QtCore.SIGNAL('clicked()'), self.executeQuery)
        self.connect(numberOfImagesSB, QtCore.SIGNAL('valueChanged(int)'), self.adjustNumberOfImages)

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
        
        self.imgName = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.currDir))
        self.queryImg.setIcon(QtGui.QIcon(self.imgName))
        label.setText(self.imgName)

    def chooseDB (self, label):
        """ Choose the image database."""
        
        self.DB = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.currDir))
        label.setText(self.DB)

        try:
            self.searcher = imagesearch.Searcher(self.DB, self.voc)
            # print 'initialized', self.searcher
        except Exception as e:
            # error = QtGui.QErrorMessage()
            # error.showMessage('Error occurred, database is not loaded.')
            print 'searcher error:', e

    def chooseMetric(self, metricName):
        """ Choose among the available similarity metrics. """

        self.metric = self.metricDict[str(metricName)]

    def adjustNumberOfImages(self, nbr_images):
        """ Adjust the number of images on users actions. """

        self.nbr_images = nbr_images
        
                      
    def executeQuery(self):
        """ Executes the given query if preconditions are met. """

        precond = self.searcher is not None \
                  and self.DB is not None \
                  and self.metric is not None \
                  and self.queryImg is not None \
                  and self.imgName is not None

        if precond:
            res = [w[1] for w in self.searcher.query(self.imgName)[:nbr_results]] # here there missing the metric
        else:
            print 'conditions are not met'
            print self.searcher,self.DB,self.metric,self.imgName

        

### Functions            

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
    
