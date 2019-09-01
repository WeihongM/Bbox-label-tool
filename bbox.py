
from bbox_widget import Ui_Form
from custom import GraphicsView, CusListItem, ImageItem
import os
from PyQt5 import QtWidgets, QtCore, QtGui, Qt

class bboxWidget(QtWidgets.QMainWindow, object):
    def __init__(self):
        super(bboxWidget, self).__init__()
        self.ui = Ui_Form()
        self.form = QtWidgets.QWidget()
        self.ui.setupUi(self.form)

        self.view = GraphicsView()
        self._scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self._scene)
        self._img = ImageItem()

        # self._img = QtWidgets.QGraphicsPixmapItem()
        # self._img.setPixmap(QtGui.QPixmap('./img/01-V001P000D.jpg'))
        self._scene.addItem(self._img)

        self.ui.gridLayout_2.addWidget(self.view, 1, 0, 1, 5)

        # btn case
        self.ui.prev_btn.clicked.connect(self.prevImages)
        self.ui.next_btn.clicked.connect(self.nextImages)
        self.ui.load_img_btn.clicked.connect(self.readImages)
        self.ui.bbox_list_edit.itemSelectionChanged.connect(self.itemSelected)
        self.ui.del_bbox_btn.clicked.connect(self.delBox)
        self.ui.tog_draw_btn.clicked.connect(self.togDrawMode)

        self._img.print_callback = self.showPrint
        self._img.pix_callback = self.showPixel
        self._img.ind_select_callback = self.setItemStatus

        self.ui.bbox_list_edit.installEventFilter(self)

        # initial variable
        self.vs = self.ui.bbox_list_edit.verticalScrollBar()
        self.current_idx = 0
        self.files = []
        self.sel = []
        self.form.setWindowTitle("Bounding Box Tool")



    def readImages(self):
        self.img_dir = QtWidgets.QFileDialog.getExistingDirectory()
        if self.img_dir:
            files = os.listdir(self.img_dir)
            for f in files:
                file, filetype = os.path.splitext(f)
                if filetype == '.jpg' or filetype == '.jpeg' or filetype == '.png':
                    self.files.append(f)
            self.current_idx = 0
            self.ui.dir_line_edit.setText(self.img_dir)
            self.showImages(self.current_idx)

    def showImages(self, idx):
        self.ui.bbox_list_edit.clear()

        filename = self.img_dir+'/'+self.files[idx]
        self._img.fromFile(filename)
        self.ui.cur_img_label.setText(str(self.current_idx+1)+" / "+str(len(self.files)))
        self.ui.file_name.setText(str(self.files[idx]))

        self._scene.setSceneRect(-self._img.pixmap.width()/2, -self._img.pixmap.height()/2, self._img.pixmap.width(), self._img.pixmap.height())
        self.view.fitInView(QtCore.QRectF(-self._img.pixmap.width()/2, -self._img.pixmap.height()/2, self._img.pixmap.width(), self._img.pixmap.height()), QtCore.Qt.KeepAspectRatio)

        self.loadAnnotation(idx)

    def prevImages(self):
        self.current_idx = self.current_idx - 1
        if(self.current_idx < 0) :
            self.current_idx = len(self.files) - 1
        self.showImages(self.current_idx)

    def nextImages(self):
        self.saveAnnotation(self._img.bboxes)
        self.current_idx = self.current_idx + 1
        if(self.current_idx >= len(self.files)) :
            self.current_idx = 0
        self.showImages(self.current_idx)

    def showPrint(self, bboxes):
        # remember scroll bar area
        self.prev_vs_val = self.vs.value()
        self.ui.bbox_list_edit.clear()

        w = self._img.pixmap.width()
        h = self._img.pixmap.height()
        for index, val in enumerate(bboxes):
            item = QtWidgets.QListWidgetItem(self.ui.bbox_list_edit)
            item_widget = CusListItem(index)
            item_widget.setLabelText(str(index))
            item_widget.setLineText(val[2])

            item_widget.setCallback = self.setClass
            item_widget.clickLineCallback = self.setItemStatus


            item.setSizeHint(item_widget.sizeHint())
            self.ui.bbox_list_edit.addItem(item)
            self.ui.bbox_list_edit.setItemWidget(item, item_widget)

        self.vs.setValue(self.prev_vs_val)


    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and event.key() == 16777220):
            # means enter key is pressed
            # source is QtWidgets.QListWidgetItem)
            # print('key press:', (event.key(), event.text()), source)
            source.itemWidget(source.selectedItems()[0]).line.setFocus()
        return super(bboxWidget, self).eventFilter(source, event)

    def setClass(self, idx, text):
        # print('change idx %s, set class %s' %(idx, text))
        self._img.setBoxClass(idx, text)

    def loadAnnotation(self, idx):
        bbox_dir = self.img_dir.replace(self.img_dir.split('/')[-1], 'label')
        if not os.path.exists(bbox_dir):
            print('label dir not created...')
        if bbox_dir:
            bbox_path_txt = bbox_dir+'/'+self.files[idx].split('.')[0]+'.txt'
            if os.path.exists(bbox_path_txt):
                f1 = open(bbox_path_txt, 'r')
                bbox_data = f1.readlines()
                self._img.bboxFromFile(bbox_data)
                f1.close()
            else:
                print('label file %s not exist...'%(self.files[idx]))

    def saveAnnotation(self, bboxes):
        save_dir = self.img_dir.replace(self.img_dir.split('/')[-1], 'label')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if save_dir:
            save_path_txt = save_dir+'/'+self.files[self.current_idx].split('.')[0]+'.txt'
            w = self._img.pixmap.width()
            h = self._img.pixmap.height()
            with open(save_path_txt, 'w') as f:
                for val in bboxes:
                    x1, y1 = val[0].x()+w/2, val[0].y()+h/2
                    x2, y2 = val[1].x()+w/2, val[1].y()+h/2
                    if len(val)==2:
                        f.write(' '+' '+'%d'%x1+' '+'%d'%y1+' '+'%d'%x2+' '+'%d'%y2+'\n')                       
                    else:
                        f.write(val[2]+' '+'%d'%x1+' '+'%d'%y1+' '+'%d'%x2+' '+'%d'%y2+'\n')

    def setItemStatus(self, idx):
        # callback function for ind_select_callback
        if idx!=None:
            this_item = self.ui.bbox_list_edit.item(idx)
            this_item.setSelected(True)
        else:
            # set selected item to False
            for selectedItem in self.ui.bbox_list_edit.selectedItems():
                selectedItem.setSelected(False)

    def delBox(self):
        if len(self.sel):
            for selectedItem in self.sel:
                # print(selectedItem.text())
                sel_idx = self.ui.bbox_list_edit.indexFromItem(selectedItem).row()
                self.ui.bbox_list_edit.takeItem(sel_idx)
                self._img.delBox(sel_idx)

    def itemSelected(self):
        # will get len()>0 when item focused, else get len()=0 when item not being focused
        self.sel = self.ui.bbox_list_edit.selectedItems()
        if len(self.sel):
            if self._img.cursor_mode and len(self.sel):
                for selectedItem in self.sel:
                    sel_idx = self.ui.bbox_list_edit.indexFromItem(selectedItem).row()
                    self._img.setSelItem(sel_idx)
        else:
            self._img.setSelItem(idx=None)

    def togDrawMode(self):
        self._img.togDrawMode()

    def showPixel(self, pos):
        w = self._img.pixmap.width()
        h = self._img.pixmap.height()
        x = pos[0]+w/2
        y = pos[1]+h/2
        self.ui.pix_pos.setText("(%d, %d)"%(x, y))

    def show(self):
        self.form.show()