#создай тут фоторедактор Easy Editor!

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout,QFileDialog
import os
app = QApplication([])
main_win = QWidget()
main_win.show()
main_win.setWindowTitle("Easy Editor")
main_win.resize(700,500)

#кнопка папка
button1=QPushButton("Папка")

#список выбора фото
listphoto=QListWidget()

#картинка
photo=QLabel("Картинка")

#набор кнопок
buttonleft=QPushButton("Лево")
buttonright=QPushButton("Право")
buttonzerkalo=QPushButton("Зеркало")
buttonrezkoct=QPushButton("Резкость")
button4b=QPushButton("Ч/Б")

line1=QVBoxLayout()
line2=QVBoxLayout()
line3=QHBoxLayout()
line4=QHBoxLayout()

line1.addWidget(button1)
line1.addWidget(listphoto)
line2.addWidget(photo)
line3.addWidget(buttonleft)
line3.addWidget(buttonright)
line3.addWidget(buttonzerkalo)
line3.addWidget(buttonrezkoct)
line3.addWidget(button4b)


line4.addLayout(line1)
line2.addLayout(line3)
line4.addLayout(line2)
main_win.setLayout(line4)

workdir= ""

class ImageProessor():
    def __init__(self):
        self.image=None
        self.currentimagename=None
        self.folder=None
        self.namefolder="photos"
    
    def showImage(self,path):
        photo.hide()
        pixmapimage=QPixmap(path)
        w,h=photo.width(), photo.height()
        pixmapimage=pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        photo.setPixmap(pixmapimage)
        photo.show()
    def loadImage(self,currentimagename):
        self.currentimagename=currentimagename
        photo=os.path.join(workdir,currentimagename)
        self.image=Image.open(photo)
    def saveImage(self):
        path=os.path.join(workdir,self.namefolder)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path=os.path.join(path, self.currentimagename)
        self.image.save(image_path)
    def do_flip(self):
        self.image=self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path=os.path.join(workdir,self.namefolder,self.currentimagename)
        self.showImage(image_path)
    def do_bw(self):
        self.image=self.image.convert("L")
        self.saveImage()
        image_path=os.path.join(workdir,self.namefolder,self.currentimagename)
        self.showImage(image_path)
    def left(self):
        self.image=self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path=os.path.join(workdir,self.namefolder,self.currentimagename)
        self.showImage(image_path)
    def right(self):
        self.image=self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path=os.path.join(workdir,self.namefolder,self.currentimagename)
        self.showImage(image_path)
    def rezkoct(self):
        self.image=self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path=os.path.join(workdir,self.namefolder,self.currentimagename)
        self.showImage(image_path)

workimage= ImageProessor()



def chooseWorkdir():
    global workdir
    workdir=QFileDialog.getExistingDirectory()

def filter(files,extensions):
    result=[]
    for photo1 in files:
        for photo2 in extensions:
            if photo1.endswith(photo2):
                result.append(photo1)
    return(result)

def showFilenamesList():
    chooseWorkdir()
    filenames=os.listdir(workdir)
    expansions=[".jpg",".png",".jpeg",".gif",".bmp"]
    save1=filter(filenames,expansions)
    listphoto.clear()
    for sa in save1:
        listphoto.addItem(sa)
button1.clicked.connect(showFilenamesList)


def showChosenImage():
    if listphoto.currentRow() >=0:
        folder= listphoto.currentItem().text()
        workimage.loadImage(folder)
        photo=os.path.join(workdir,workimage.currentimagename)
        workimage.showImage(photo)
listphoto.currentRowChanged.connect(showChosenImage)
buttonzerkalo.clicked.connect(workimage.do_flip)
button4b.clicked.connect(workimage.do_bw)
buttonleft.clicked.connect(workimage.left)
buttonright.clicked.connect(workimage.right)
buttonrezkoct.clicked.connect(workimage.rezkoct)
app.exec_()