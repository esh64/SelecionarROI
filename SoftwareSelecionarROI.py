import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QMainWindow, QAction, qApp, QApplication, QFileDialog, QGridLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QDesktopServices
import pickle

class Label(QLabel):
    def __init__(self, parent=None):
        super(Label, self).__init__(parent=parent)
        self.point1Roi=None
        self.point2Roi=None
        self.point1fio1=None
        self.point2fio1=None
        self.point1fio2=None
        self.point2fio2=None
        self.point1fio3=None
        self.point2fio3=None
        self.currentPosition2=None
        self.workingNow=None
    
    def paintEvent(self, e):
        super().paintEvent(e)
        qp = QPainter(self)
        pen=QPen(Qt.red, 5, Qt.SolidLine)
        qp.setPen(pen)
        if type(self.point1Roi)!=type(None) and type(self.point2Roi)!=type(None):
            qp.drawLine(self.point1Roi['x'], self.point1Roi['y'], self.point1Roi['x'], self.point2Roi['y'])
            qp.drawLine(self.point2Roi['x'], self.point1Roi['y'], self.point2Roi['x'], self.point2Roi['y'])
            qp.drawLine(self.point1Roi['x'], self.point1Roi['y'], self.point2Roi['x'], self.point1Roi['y'])
            qp.drawLine(self.point1Roi['x'], self.point2Roi['y'], self.point2Roi['x'], self.point2Roi['y'])
        if type(self.point1fio1)!=type(None) and type(self.point2fio1)!=type(None):
            qp.drawLine(self.point1fio1['x'], self.point1fio1['y'], self.point2fio1['x'], self.point2fio1['y'])
        if type(self.point1fio2)!=type(None) and type(self.point2fio2)!=type(None):
            qp.drawLine(self.point1fio2['x'], self.point1fio2['y'], self.point2fio2['x'], self.point2fio2['y'])
        if type(self.point1fio3)!=type(None) and type(self.point2fio3)!=type(None):
            qp.drawLine(self.point1fio3['x'], self.point1fio3['y'], self.point2fio3['x'], self.point2fio3['y'])


class PictureToSelectRoi(QWidget):
    def __init__(self):
        super(PictureToSelectRoi,self).__init__()
        #images buttons
        self.roiButton = QPushButton("ROI")
        self.roiButton.clicked[bool].connect(self.clickedButtonROI)
        self.roiButton.setStyleSheet("background-color: white")
        self.fio1Button = QPushButton("Fio 1")
        self.fio1Button.clicked[bool].connect(self.clickedButtonFIO1)
        self.fio1Button.setStyleSheet("background-color: white")
        self.fio2Button = QPushButton("Fio 2")
        self.fio2Button.clicked[bool].connect(self.clickedButtonFIO2)
        self.fio2Button.setStyleSheet("background-color: white")
        self.fio3Button = QPushButton("Fio 3")
        self.fio3Button.clicked[bool].connect(self.clickedButtonFIO3)
        self.fio3Button.setStyleSheet("background-color: white")
        
        #scroll area
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        
        #-----Layout
        
        #vertical layout
        vbox = QVBoxLayout()
        #vbox.addStretch(1)
        
        #horizontal layout
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.roiButton)
        hbox.addWidget(self.fio1Button)
        hbox.addWidget(self.fio2Button)
        hbox.addWidget(self.fio3Button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.scroll)
        
        self.setLayout(vbox) 
        
        #---fim layout

        #label
        self.label = Label(self)
        self.label.mousePressEvent=self.mouseReleaseEvent2
        self.label.mouseMoveEvent=self.mouseMoveEvent2
        self.scroll.setWidget(self.label)
        
        #atributes
        self.pressedButton=None
        self.imageOpened=False
        self.countClick=0
        self.roiPoint1=None
        self.roiPoint2=None
        
    def mouseReleaseEvent2(self, QMouseEvent):
        if self.imageOpened:
            if self.countClick==0:
                self.countClick=1
                
                if self.pressedButton=="ROI":
                    self.label.point1Roi={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                    self.label.point2Roi=None
                elif self.pressedButton=="FIO1":
                    self.label.point1fio1={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                    self.label.point2fio1=None
                elif self.pressedButton=="FIO2":
                    self.label.point1fio2={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                    self.label.point2fio2=None
                elif self.pressedButton=="FIO3":
                    self.label.point1fio3={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                    self.label.point2fio3=None
            elif self.countClick==1:
                self.countClick=0
                if self.pressedButton=="ROI":
                    #self.label.point1Roi=self.roiPoint1
                    self.label.point2Roi={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                elif self.pressedButton=="FIO1":
                    #self.label.point1fio1=self.roiPoint1
                    self.label.point2fio1={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                elif self.pressedButton=="FIO2":
                    #self.label.point1fio2=self.roiPoint1
                    self.label.point2fio2={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                elif self.pressedButton=="FIO3":
                    #self.label.point1fio3=self.roiPoint1
                    self.label.point2fio3={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                self.label.update()
    
    def mouseMoveEvent2(self, QMouseEvent):
        if self.imageOpened:
            if self.countClick==1:
                if self.pressedButton=="ROI":
                    self.label.point2Roi={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                elif self.pressedButton=="FIO1":
                    self.label.point2fio1={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                elif self.pressedButton=="FIO2":
                    self.label.point2fio2={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
                elif self.pressedButton=="FIO3":
                    self.label.point2fio3={'x':QMouseEvent.x(), 'y':QMouseEvent.y()}
            self.label.update()
    
    def clickedButtonROI(self, pressed):
        if self.pressedButton=="ROI":
            self.label.workingNow=None
            self.roiButton.setStyleSheet("background-color: white")
        elif self.pressedButton==None:
            self.pressedButton="ROI"
            self.roiButton.setStyleSheet("background-color: red")
        else:
            self.pressedButton="ROI"
            self.roiButton.setStyleSheet("background-color: red")
            self.fio1Button.setStyleSheet("background-color: white")
            self.fio2Button.setStyleSheet("background-color: white")
            self.fio3Button.setStyleSheet("background-color: white")
        self.label.workingNow=self.pressedButton
            
    def clickedButtonFIO1(self, pressed):
        if self.pressedButton=="FIO1":
            self.pressedButton=None
            self.fio1Button.setStyleSheet("background-color: white")
        elif self.pressedButton==None:
            self.pressedButton="FIO1"
            self.fio1Button.setStyleSheet("background-color: red")
        else:
            self.pressedButton="FIO1"
            self.fio1Button.setStyleSheet("background-color: red")
            self.roiButton.setStyleSheet("background-color: white")
            self.fio2Button.setStyleSheet("background-color: white")
            self.fio3Button.setStyleSheet("background-color: white")
        self.label.workingNow=self.pressedButton

    def clickedButtonFIO2(self, pressed):
        if self.pressedButton=="FIO2":
            self.pressedButton=None
            self.fio2Button.setStyleSheet("background-color: white")
        elif self.pressedButton==None:
            self.pressedButton="FIO2"
            self.fio2Button.setStyleSheet("background-color: red")
        else:
            self.pressedButton="FIO2"
            self.fio2Button.setStyleSheet("background-color: red")
            self.roiButton.setStyleSheet("background-color: white")
            self.fio1Button.setStyleSheet("background-color: white")
            self.fio3Button.setStyleSheet("background-color: white")
        self.label.workingNow=self.pressedButton

    def clickedButtonFIO3(self, pressed):
        if self.pressedButton=="FIO3":
            self.pressedButton=None
            self.fio3Button.setStyleSheet("background-color: white")
        elif self.pressedButton==None:
            self.pressedButton="FIO3"
            self.fio3Button.setStyleSheet("background-color: red")
        else:
            self.pressedButton="FIO3"
            self.fio3Button.setStyleSheet("background-color: red")
            self.roiButton.setStyleSheet("background-color: white")
            self.fio2Button.setStyleSheet("background-color: white")
            self.fio1Button.setStyleSheet("background-color: white")
        self.label.workingNow=self.pressedButton
        
class SelecionadorROI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.openedImageFilename=''
        self.initUI()
        
        
    def initUI(self):
        
        #----------------------menu options
        
        #--file menu options
        
        #exit option
        exitAct = QAction(QIcon(''), '&Sair', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Sair do aplicativo')
        exitAct.triggered.connect(qApp.quit)

        #open image option
        openAct = QAction(QIcon(''), '&Abrir', self)        
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Abrir imagem')
        openAct.triggered.connect(self.openFileNameDialog)
    
        #save coordinates option
        saveAct = QAction(QIcon(''), '&Salvar', self)        
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Salvar as coordenadas')
        saveAct.triggered.connect(self.file_save)
        
        ##--About menu options
        #aboutAct = QAction(QIcon(''), '&Sobre', self)        
        #aboutAct.setStatusTip('Sobre o Programa')
        #aboutAct.triggered.connect(QDesktopServices.openUrl(Qt.QUrl('https://github.com/esh64/SelecionarROI/blob/master/README.md')))
        
        #menu bar
        self.menubar = self.menuBar()
        
        #file menu
        self.fileMenu = self.menubar.addMenu('&Arquivo')
        self.fileMenu.addAction(openAct)
        self.fileMenu.addAction(saveAct)
        self.fileMenu.addAction(exitAct)
        
        ##help menu
        #self.helpMenu = self.menubar.addMenu('&Ajuda')
        #self.helpMenu.addAction(aboutAct)
        
        #--------------End menu
        
        self.picture=PictureToSelectRoi()
        self.setCentralWidget(self.picture)
        
        #statusBar()
        self.statusBar().showMessage('Abra uma imagem')
    
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('SelecionadorROI')    
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.openedImageFilename, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
        if self.openedImageFilename:
            pixmap = QPixmap(self.openedImageFilename)
            self.picture.label.setPixmap(pixmap)
            self.picture.label.resize(pixmap.width(),pixmap.height())
            self.picture.imageOpened=True
            self.statusBar().showMessage('Image opened')
    
    def file_save(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save File')
        if fileName[0]!='':
            roi={'point1':self.picture.label.point1Roi, 'point2':self.picture.label.point2Roi}
            fio1={'point1':self.picture.label.point1fio1, 'point2':self.picture.label.point2fio1}
            fio2={'point1':self.picture.label.point1fio2, 'point2':self.picture.label.point2fio2}
            fio3={'point1':self.picture.label.point1fio3, 'point2':self.picture.label.point2fio3}
            areas={'roi':roi, 'fio1':fio1, 'fio2':fio2, 'fio3':fio3}
            pickle.dump(areas, open(fileName[0]+'.roi', 'wb'))
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SelecionadorROI()
    sys.exit(app.exec_())

