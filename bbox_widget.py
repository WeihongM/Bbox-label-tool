# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bbox_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1040, 740)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.dir_line_edit = QtWidgets.QLineEdit(Form)
        self.dir_line_edit.setObjectName("dir_line_edit")
        self.gridLayout.addWidget(self.dir_line_edit, 0, 1, 1, 1)
        self.bbox_group = QtWidgets.QGroupBox(Form)
        self.bbox_group.setObjectName("bbox_group")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.bbox_group)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.bbox_list_edit = QtWidgets.QListWidget(self.bbox_group)

        self.bbox_list_edit.setStyleSheet( """
                                QListWidget:item:selected:!disabled {
                                     background: #00BFFF;
                                }
                                """
                                )        

        self.bbox_list_edit.setObjectName("bbox_list_edit")
        self.gridLayout_3.addWidget(self.bbox_list_edit, 0, 0, 1, 1)
        self.del_bbox_btn = QtWidgets.QPushButton(self.bbox_group)
        self.del_bbox_btn.setObjectName("del_bbox_btn")
        self.gridLayout_3.addWidget(self.del_bbox_btn, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.bbox_group, 1, 2, 1, 1)
        self.dir_label = QtWidgets.QLabel(Form)
        self.dir_label.setObjectName("dir_label")
        self.gridLayout.addWidget(self.dir_label, 0, 0, 1, 1)
        self.img_group = QtWidgets.QGroupBox(Form)
        self.img_group.setObjectName("img_group")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.img_group)
        self.gridLayout_2.setHorizontalSpacing(100)
        self.gridLayout_2.setVerticalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.file_name = QtWidgets.QLabel(self.img_group)
        self.file_name.setObjectName("file_name")
        self.gridLayout_2.addWidget(self.file_name, 0, 0, 1, 1)
        self.pix_pos = QtWidgets.QLabel(self.img_group)
        self.pix_pos.setObjectName("pix_pos")
        self.gridLayout_2.addWidget(self.pix_pos, 0, 4, 1, 1)
        self.prev_btn = QtWidgets.QPushButton(self.img_group)
        self.prev_btn.setObjectName("prev_btn")
        self.gridLayout_2.addWidget(self.prev_btn, 3, 0, 1, 1)
        self.cur_img_label = QtWidgets.QLabel(self.img_group)
        self.cur_img_label.setObjectName("cur_img_label")
        self.gridLayout_2.addWidget(self.cur_img_label, 3, 2, 1, 1)
        self.next_btn = QtWidgets.QPushButton(self.img_group)
        self.next_btn.setObjectName("next_btn")
        self.gridLayout_2.addWidget(self.next_btn, 3, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 3, 3, 1, 1)
        self.gridLayout.addWidget(self.img_group, 1, 0, 2, 2)
        self.tog_draw_btn = QtWidgets.QPushButton(Form)
        self.tog_draw_btn.setObjectName("tog_draw_btn")
        self.gridLayout.addWidget(self.tog_draw_btn, 2, 2, 1, 1)
        self.load_img_btn = QtWidgets.QPushButton(Form)
        self.load_img_btn.setObjectName("load_img_btn")
        self.gridLayout.addWidget(self.load_img_btn, 0, 2, 1, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.bbox_group.setTitle(_translate("Form", "Bounding box"))
        self.del_bbox_btn.setText(_translate("Form", "Del bbox"))
        self.dir_label.setText(_translate("Form", "Img Dir:"))
        self.img_group.setTitle(_translate("Form", "GroupBox"))
        self.file_name.setText(_translate("Form", "TextLabel"))
        self.pix_pos.setText(_translate("Form", "TextLabel"))
        self.prev_btn.setText(_translate("Form", "Prev"))
        self.cur_img_label.setText(_translate("Form", "TextLabel"))
        self.next_btn.setText(_translate("Form", "Next"))
        self.tog_draw_btn.setText(_translate("Form", "Write/Draw"))
        self.load_img_btn.setText(_translate("Form", "Load Dir"))