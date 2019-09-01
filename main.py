import sys
import bbox
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    box = bbox.bboxWidget()
    box.show()
    sys.exit(app.exec_())