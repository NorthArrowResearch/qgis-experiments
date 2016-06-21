# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NARDemoPluginDockWidget
                                 A QGIS plugin
 Demo Plugin
                             -------------------
        begin                : 2016-06-20
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Matt
        email                : matt@northarrowreseawrch.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from subtract import SubtractWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'demo_plugin_dockwidget_base.ui'))


class NARDemoPluginDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(NARDemoPluginDockWidget, self).__init__(parent)
        self.iface = iface
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.subtractDialog = SubtractWidget(iface)
        self.btnLoadXML.clicked.connect(self.file_browser)
        self.btnSubtract.clicked.connect(self.subtractEvent)

    def file_browser(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Open file", "", "XML File (*.xml);;All files (*)")
        filename = os.path.splitext(str(filename))[0]+".xml"
        layer_name = os.path.splitext(os.path.basename(str(filename)))[0]
        if layer_name == ".tiff":
            return
        print "BOOYA: " + filename

    def subtractEvent(self, event):
        self.subtractDialog.exec_()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

