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
from PyQt4.QtCore import *
from qgis.core import QgsMapLayer, QgsRasterLayer, QgsMapLayerRegistry,QgsProject
from classes import Raster

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'setnull.ui'))


class EuclidDistWidget(QtGui.QDialog, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(EuclidDistWidget, self).__init__(parent)
        self.iface = iface
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.btnLoad.clicked.connect(self.raster_file_browser)

        # Set some initial setup
        last_index1 = self.cb_input1.currentText()
        # populate the combo box with the polygon layers listed in the current legend
        self.set_input_layer_combobox(self.cb_input1, last_index1)

        # Recalc the state of the UI buttons
        self.cb_input1.currentIndexChanged.connect(self.recalc_state)
        self.lineEdit.textEdited.connect(self.recalc_state)

        self.buttonBox.clicked.connect(self.on_click)
        self.recalc_state(None)

    def get_raster_layers(self, skip_active=False):
        """
        Returns a dict of layers [name: id] in the project

        :return: dict of layers with given geometry type
        """
        layer_list = {}
        for layer in self.iface.legendInterface().layers():
            if QgsMapLayer.RasterLayer == layer.type():   # vectorLayer
                layer_list[layer.name()] = layer.id()
                            
        return layer_list

    def set_input_layer_combobox(self, cbBox, item=''):
        """
        Populates the ComboBox with all layers of the given geometry type geom_type, and sets
        currentIndex to the entry named index.

        :param index: string; name of the ComboBox entry to set currentIndex to
        :return: None
        """
        cbBox.clear()
        layer_list = self.get_raster_layers(False)
        if len(layer_list) > 0:
            for index, aName in enumerate(layer_list):
                cbBox.addItem('')
                cbBox.setItemText(index, aName)
                if aName == item:
                    cbBox.setCurrentIndex(index)
        return None
        
    def raster_file_browser(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Open file", "", "RasterFile (*.tiff);;All files (*)")
        filename = os.path.splitext(str(filename))[0]+".tiff"
        layer_name = os.path.splitext(os.path.basename(str(filename)))[0]
        if layer_name == ".tiff":
            return
        self.lineEdit.setText(filename)
        self.recalc_state(None)

    def on_click(self, button):
        if QtGui.QDialogButtonBox.Cancel == self.buttonBox.standardButton(button):
            self.done(QtGui.QDialog.Rejected)
        elif QtGui.QDialogButtonBox.Ok == self.buttonBox.standardButton(button):
            self.raster_setNull()
            self.done(QtGui.QDialog.Accepted)
        elif QtGui.QDialogButtonBox.Help == self.buttonBox.standardButton(button):
            QtGui.QDesktopServices.openUrl(QUrl("http://slashdot.org"))
        elif QtGui.QDialogButtonBox.Reset == self.buttonBox.standardButton(button):
            self.cb_input1.setCurrentIndex(-1)
            self.lineEdit.setText("")

    def recalc_state(self, event):
        if self.cb_input1.currentIndex() > -1 and len(self.lineEdit.text()) > 0:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

    def raster_setNull(self):
        # if the layer does not exist it has to be created
        rlayer1 = QgsMapLayerRegistry.instance().mapLayersByName(self.cb_input1.currentText())[0]
        textEq = self.txtEq.text()
        fileName = self.lineEdit.text()

        import parser
        formula = "sin(x)*x**2"
        code = parser.expr(formula).compile()

        from math import sin
        x = 10
        print eval(code)

        templateRaster = Raster(rlayer1.source())

        width, height = templateRaster.band_array.shape  # or width = raster.width and height = raster.height()
        print width
        print height
        # and
        for row in range(0, width):
            for col in range(0, height):
                print row, col, templateRaster.band_array[row, col]

        # Load the file into the map
        # fileInfo = QFileInfo(fileName)
        # baseName = fileInfo.baseName()
        #
        # root = QgsProject.instance().layerTreeRoot()
        # node_group1 = root.insertGroup(0, "Group 1")
        # node_subgroup1 = node_group1.addGroup("Sub-group 1")

        # Check out signals from nodes section
        # http://www.lutraconsulting.co.uk/blog/2014/07/25/qgis-layer-tree-api-part-2/

        # if the layer does not exist it has to be created
        # if not QgsMapLayerRegistry.instance().mapLayersByName(baseName):
        #     rOutput = QgsRasterLayer(fileName, baseName)
        #     QgsMapLayerRegistry.instance().addMapLayer(rOutput, False)
        #     node_layer1 = node_subgroup1.addLayer(rOutput)

        # if the layer already exists trigger a refresh
        # else:
        #     rOutput = QgsMapLayerRegistry.instance().mapLayersByName(baseName)[0]
        #     rOutput.triggerRepaint()


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

