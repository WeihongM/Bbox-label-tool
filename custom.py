
from PyQt5 import QtWidgets, QtGui, QtCore
import math

class GraphicsView(QtWidgets.QGraphicsView):
    dragMode = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        # initial setting
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        self.scale(factor, factor)


class CusLineEdit(QtWidgets.QLineEdit):
    lineClickSignal = QtCore.pyqtSignal()
    focusSignal = QtCore.pyqtSignal()

    def __init__(self, value):
        super(CusLineEdit, self).__init__(value)

    def mousePressEvent(self, event):
        # print('mouse Press event')
        self.lineClickSignal.emit()

    def focusInEvent(self, event):
        # print ('focus in event')
        self.focusSignal.emit()
        # do custom stuff
        super(CusLineEdit, self).focusInEvent(event)


class CusListItem(QtWidgets.QWidget):
    def __init__(self, index, parent=None):
        super(CusListItem, self).__init__(parent)
        self.label = QtWidgets.QLabel()
        # self.line = QtWidgets.QLineEdit()
        self.line = CusLineEdit('')
        f = self.line.font()
        f.setPointSize(20)
        self.line.setFont(f)

        self.num = index
        self.setCallback = None
        self.clickLineCallback = None

        self.line.textChanged.connect(self.setClass)
        self.line.lineClickSignal.connect(self.setClickLine)
        self.line.focusSignal.connect(self.setClickLine)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        self.setLayout(layout)

    def setLabelText(self, str):
        self.label.setText(str)

    def setLineText(self, str):
        self.line.setText(str)

    def setClass(self):
        if self.setCallback!=None:
            self.setCallback(self.num, self.line.text())

    def setClickLine(self):
        # print('%d num is clicked' %self.num)
        if self.clickLineCallback!=None:
            self.clickLineCallback(self.num)


class ImageItem(QtWidgets.QGraphicsItem):

    def __init__(self, parent=None):
        super(ImageItem, self).__init__(parent)

        # initial setting
        self.setAcceptHoverEvents(True)

        # initial variable
        self.pixmap = QtGui.QPixmap()
        # self.pixmap = QtGui.QPixmap.fromImage(QtGui.QImage('./img/image.jpg'))
        self.bboxes = []                    # index(0,1,2) -> (start point coor, end point coor, class)
        self.box_start = QtCore.QPointF()
        self.box_end = QtCore.QPointF()
        self.hover_pos = QtCore.QPointF()
        self.click = 0
        self.print_callback = None          # print all box label into QlistWidget
        self.pix_callback = None
        self.ind_select_callback = None     # set the QListWidget item status
        self.cursor_mode = True
        self.draw_box = False
        self.click_box = None               # store the mouseclick QPointF
        self.sel_item_ind = None

        self.focus_char = []

    def fromFile(self, str):
        self.pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(str))
        del self.bboxes[:]
        self.scene().update()

    def togDrawMode(self):
        self.cursor_mode = not self.cursor_mode

    def bboxFromFile(self, bbox_data):
        for line in bbox_data:
            val = line.strip().split(' ')
            w = self.pixmap.width()
            h = self.pixmap.height()
            if len(val) == 5:
                class_ = val[0]
                left = float(val[1])
                top = float(val[2])
                right = float(val[3])
                bottom = float(val[4])
                spt = QtCore.QPointF(left-w/2, top-h/2)
                ept = QtCore.QPointF(right-w/2, bottom-h/2)
                self.bboxes.append([spt, ept, class_])
            elif len(val) == 4:
                left = float(val[0])
                top = float(val[1])
                right = float(val[2])
                bottom = float(val[3])
                spt = QtCore.QPointF(left-w/2, top-h/2)
                ept = QtCore.QPointF(right-w/2, bottom-h/2)
                self.bboxes.append([spt, ept, ''])
        if self.print_callback != None:
            self.print_callback(self.bboxes)

    def setBoxClass(self, idx, class_):
        # set box class after edit on the QListwidget
        self.bboxes[idx][2] = class_

    def setSelItem(self, idx):
        if idx!=None:
            self.sel_item_ind = idx
            self.click_box = None       # sel item means no click on the image(avoid crash in paint function)
            # print('3')
        else:
            self.sel_item_ind = None
        self.update()

    def delBox(self, idx):
        self.bboxes.pop(idx)
        self.update()
        # renew content in the QListwidget
        if self.print_callback != None:
            self.print_callback(self.bboxes)

    def paint(self, painter, option, widget):
        w = self.pixmap.width()
        h = self.pixmap.height()
        pt = QtCore.QPointF(-w/2, -h/2)

        # draw pixmap into scene
        if not self.pixmap.isNull():
            painter.drawPixmap(pt, self.pixmap)
            if not self.cursor_mode:
                x = min(self.hover_pos.x(),w/2)
                x = max(x, -w/2)
                y = min(self.hover_pos.y(),h/2)
                y = max(y, -h/2)
                hover_line_x = QtCore.QLineF(x,-h/2,x,h/2)
                hover_line_y = QtCore.QLineF(-w/2,y,w/2,y)
                # brush = QtGui.QBrush(QtGui.QColor(0,0,0))
                painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0),0.75*w/320.,QtCore.Qt.SolidLine))
                painter.drawLine(hover_line_x)
                painter.drawLine(hover_line_y)
        # draw moving mouse box
        if self.draw_box:
            # brush = QtGui.QBrush(QtGui.QColor(255,0,0))
            painter.setPen(QtGui.QPen(QtGui.QColor(255,0,0),0.75*w/320.,QtCore.Qt.SolidLine))
            painter.drawRect(QtCore.QRectF(self.box_start,self.box_end))
        # show all drawed box
        for ind, box in enumerate(self.bboxes):
            rect =  QtCore.QRectF(box[0], box[1])
            if box[2] not in self.focus_char:
                painter.setPen(QtGui.QPen(QtGui.QColor(178,34,34),0.4*w/320.,QtCore.Qt.SolidLine))
                painter.drawRect(rect)
            else:
                painter.setPen(QtGui.QPen(QtGui.QColor(70,130,180),0.4*w/320.,QtCore.Qt.SolidLine))
                painter.drawRect(rect)
            # font = QtGui.QFont("ubuntu",6.*w/320.)
            # painter.setFont(font)
            # painter.drawText(rect.x(), rect.y(), str(ind))
        # show the region and their corresponding item when item selected or mouse click on the region
        if self.cursor_mode:
            if self.click_box!=None:
                chose_ind = None
                for index, b in enumerate(self.bboxes):
                    if b[0].x()<self.click_box.x()<b[1].x() and \
                    b[0].y()<self.click_box.y()<b[1].y():
                        brush = QtGui.QBrush(QtGui.QColor(0,0,0, 100))
                        painter.setBrush(brush)
                        chose_rect = QtCore.QRectF(b[0], b[1])
                        chose_ind = index
                        painter.drawRect(chose_rect)
                        # print('2')
                if self.ind_select_callback!=None:
                    self.ind_select_callback(chose_ind)
            elif self.click_box==None and self.sel_item_ind!=None:
                brush = QtGui.QBrush(QtGui.QColor(255,0,0, 100))
                painter.setBrush(brush)
                tmp = QtCore.QRectF(self.bboxes[self.sel_item_ind][0], self.bboxes[self.sel_item_ind][1])
                painter.drawRect(tmp)                
                # print('4')
        else:
            if self.ind_select_callback!=None:
                self.ind_select_callback(None)

    def boundingRect(self):
        w = self.pixmap.width()
        h = self.pixmap.height()
        o = 300
        rect = QtCore.QRectF(-w/2,-h/2,w,h)
        return rect

    def mousePressEvent(self, event):
        # print('ImageItem mouse press')
        if not self.cursor_mode:
            self.click = 1 - self.click
            if self.click:
                self.draw_box = True
                self.box_start = event.pos()
                self.box_end = event.pos()
            else:
                self.draw_box = False
                if self.box_start != self.box_end:
                    x_start = min(self.box_start.x(), self.box_end.x())
                    y_start = min(self.box_start.y(), self.box_end.y())
                    x_end = max(self.box_start.x(), self.box_end.x())
                    y_end = max(self.box_start.y(), self.box_end.y())
                    start = QtCore.QPointF(x_start, y_start)
                    end = QtCore.QPointF(x_end, y_end)
                    self.bboxes.append([start, end, ''])
                # show all box label into listWidget
                if self.print_callback != None:
                    self.print_callback(self.bboxes)
        elif self.cursor_mode and len(self.bboxes):
            self.click_box = event.pos()
            # print('1')
        self.update()

    def mouseMoveEvent(self, event):
        if self.draw_box:
            self.box_end = event.pos()
            self.update()

    def hoverMoveEvent(self, event):
        self.hover_pos = event.pos()
        if self.pix_callback != None:
            pix_pos = (self.hover_pos.x(), self.hover_pos.y())
            self.pix_callback(pix_pos)
        if self.draw_box:
            self.box_end = event.pos()
        if not self.cursor_mode:
            self.update()