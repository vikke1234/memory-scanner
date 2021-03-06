# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.amount_found = QtWidgets.QLabel(self.centralwidget)
        self.amount_found.setObjectName("amount_found")
        self.verticalLayout_4.addWidget(self.amount_found)
        self.found_table = QtWidgets.QTableView(self.centralwidget)
        self.found_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.found_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.found_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.found_table.setAlternatingRowColors(True)
        self.found_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.found_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.found_table.setShowGrid(False)
        self.found_table.setGridStyle(QtCore.Qt.NoPen)
        self.found_table.setObjectName("found_table")
        self.verticalLayout_4.addWidget(self.found_table)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.scan_widget = QtWidgets.QWidget(self.centralwidget)
        self.scan_widget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scan_widget.sizePolicy().hasHeightForWidth())
        self.scan_widget.setSizePolicy(sizePolicy)
        self.scan_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.scan_widget.setObjectName("scan_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scan_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scan_layout = QtWidgets.QVBoxLayout()
        self.scan_layout.setObjectName("scan_layout")
        self.search_button_layout = QtWidgets.QHBoxLayout()
        self.search_button_layout.setObjectName("search_button_layout")
        self.new_scan = QtWidgets.QPushButton(self.scan_widget)
        self.new_scan.setEnabled(True)
        self.new_scan.setObjectName("new_scan")
        self.search_button_layout.addWidget(self.new_scan)
        self.next_scan = QtWidgets.QPushButton(self.scan_widget)
        self.next_scan.setEnabled(False)
        self.next_scan.setObjectName("next_scan")
        self.search_button_layout.addWidget(self.next_scan)
        self.undo_scan = QtWidgets.QPushButton(self.scan_widget)
        self.undo_scan.setEnabled(False)
        self.undo_scan.setObjectName("undo_scan")
        self.search_button_layout.addWidget(self.undo_scan)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.search_button_layout.addItem(spacerItem)
        self.scan_layout.addLayout(self.search_button_layout)
        self.search_for = QtWidgets.QLineEdit(self.scan_widget)
        self.search_for.setEnabled(True)
        self.search_for.setObjectName("search_for")
        self.scan_layout.addWidget(self.search_for)
        self.scan_matching = QtWidgets.QComboBox(self.scan_widget)
        self.scan_matching.setEnabled(True)
        self.scan_matching.setObjectName("scan_matching")
        self.scan_matching.addItem("")
        self.scan_matching.addItem("")
        self.scan_matching.addItem("")
        self.scan_matching.addItem("")
        self.scan_layout.addWidget(self.scan_matching)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.scan_byte_size = QtWidgets.QComboBox(self.scan_widget)
        self.scan_byte_size.setEnabled(True)
        self.scan_byte_size.setObjectName("scan_byte_size")
        self.horizontalLayout_7.addWidget(self.scan_byte_size)
        self.aligned = QtWidgets.QCheckBox(self.scan_widget)
        self.aligned.setChecked(True)
        self.aligned.setObjectName("aligned")
        self.horizontalLayout_7.addWidget(self.aligned)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.scan_layout.addLayout(self.horizontalLayout_7)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scan_layout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.scan_layout)
        self.horizontalLayout_4.addWidget(self.scan_widget)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.saved_results = SavedAddressView(self.centralwidget)
        self.saved_results.setEnabled(True)
        self.saved_results.setObjectName("saved_results")
        self.verticalLayout_6.addWidget(self.saved_results)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setEnabled(True)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAttach = QtWidgets.QAction(MainWindow)
        self.actionAttach.setEnabled(True)
        self.actionAttach.setObjectName("actionAttach")
        self.menuFile.addAction(self.actionAttach)
        self.menubar.addAction(self.menuFile.menuAction())
        self.amount_found.setBuddy(self.found_table)

        self.retranslateUi(MainWindow)
        self.scan_byte_size.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.amount_found.setToolTip(_translate("MainWindow", "A max of 100 000 entries will be shown at a time"))
        self.amount_found.setText(_translate("MainWindow", "Found: 0"))
        self.new_scan.setText(_translate("MainWindow", "New scan"))
        self.next_scan.setText(_translate("MainWindow", "Next scan"))
        self.undo_scan.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Currently not available</p></body></html>"))
        self.undo_scan.setText(_translate("MainWindow", "Undo scan"))
        self.search_for.setPlaceholderText(_translate("MainWindow", "Search"))
        self.scan_matching.setItemText(0, _translate("MainWindow", "Exact value"))
        self.scan_matching.setItemText(1, _translate("MainWindow", "Greater than"))
        self.scan_matching.setItemText(2, _translate("MainWindow", "Less than"))
        self.scan_matching.setItemText(3, _translate("MainWindow", "Not equal"))
        self.aligned.setText(_translate("MainWindow", "Aligned"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAttach.setText(_translate("MainWindow", "Attach"))
        self.actionAttach.setToolTip(_translate("MainWindow", "Attach to a process"))
        self.actionAttach.setStatusTip(_translate("MainWindow", "Disabled if you\'re not root"))
        self.actionAttach.setWhatsThis(_translate("MainWindow", "Disabled if you\'re not root"))
        self.actionAttach.setShortcut(_translate("MainWindow", "F2"))
from gui.views.saved_address_view import SavedAddressView
