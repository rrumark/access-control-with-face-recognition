from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


import sys

import numpy as np

from database_ import Database
from video_ import videLogin   





class Main(QMainWindow):
    
    def __init__(self):
        super(Main, self).__init__()
        self.setFixedSize(576,360)
        
        self.Video = videLogin() # videpLogin sınıfı
        self.DB = Database()     # Database sınıfı

        # Arayüz penceresi açıldığında monitörün merkezinde konunlanması için
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


        self.usernameLineEdit = QLineEdit(self)
        self.usernameLineEdit.setPlaceholderText('username')
        self.usernameLineEdit.setFocus()
        self.usernameLineEdit.setFixedWidth(215)

        self.loginButton = QPushButton("Login", self)

        # Arayüzde ki login görselini arayüze aktarmak için.
        self.pixmap = QPixmap('photos/login.png')
        self.loginImage = QLabel(self)
        self.loginImage.setPixmap(self.pixmap)
        self.loginImage.resize(self.pixmap.width(), self.pixmap.height())

        # Arayüz elemanlarının formda ki konumlandırmaları
        self.loginImage.move(390, 70)
        self.usernameLineEdit.move(335,200)
        self.loginButton.move(450, 250)

        
        self.applyThema() # Arayüz elemanlarının ve arkaplanın oluşturulduğu fonk.
   


        #
        self.loginButton.clicked.connect(self.clickLoginButton) 
        
        self.show()




        
    def applyThema(self):

        # Arayüzde arkaplan görseli
        self.setStyleSheet("QMainWindow {background-image : url(photos/back.jpg);}") 

        # Login buton tasarımı
        self.loginButton.setStyleSheet("QPushButton {Background-color: #000229 ;color: #DBDBDD; border-radius: 5px;}"
                                    "QPushButton::pressed { Background-color: #0E3C59; color: #B4B5BF;}")
        # username LineEdit tasarımı
        self.usernameLineEdit.setStyleSheet("QLineEdit {border-radius: 5px; border-style: outset; border-width: 1.5px; border-color: #000229; padding: 2px;}")


        

    # Login butona tıkladığında yapılacak işemler 
    def clickLoginButton(self):

        self.pleaseWait() # Please Wait uyarısı

        userName = self.usernameLineEdit.text() # username LineEdit deki text değeri (yani username değeri)
        imageData = self.DB.databaseExtraction(userName) # username adlı tabloyu veri tabanından çekiyoruz.

        if imageData == False: # Eğer veri tabanında girilen değere göre tablo yoksa hata mesajı gösteriyor.
            self.DialogWin.close() # Please Wait uyuarısını kapat
            self.errorMessage()

        else: # Tablo mevcut ise
            img = self.DB.get2Dto3D(imageData) # Veri tabanından çekilen veri karşılaştırma için uygun hale getiriliyor.

            self.DialogWin.close() # Please Wait uyuarısını kapat

            self.Video.showVideo(img) # Video penceresi açılıyor ve uygun hale getirilen veri 'r' ya da 'r' tuşuna basıldğında karşılaştırma başlıyor.

            if self.Video.getStatu(): # Karşılaştırma doğru ise giriş başarılı uyarısı çıkuyor.
                self.informationMessage()

            else: # Karşılaştırma yanlış ise giriş başarısız uyarısı çıkuyor.
                self.errorMessage(text = "Login failed!!!              ")
                


    # Please Wait uyarısnının 
    def pleaseWait(self): 

        self.DialogWin = QDialog()
        self.DialogWin.setWindowFlags(Qt.FramelessWindowHint)
        self.DialogWin.setFixedSize(350,75)
        self.DialogWin.setWindowModality(Qt.ApplicationModal)
        self.DialogWin.setStyleSheet("Background-color: #000229; color: #DBDBDD;")
        HBox = QHBoxLayout()
        HBox.addStretch()
        HBox.addWidget(QLabel("Please wait"))
        HBox.addStretch()
        self.DialogWin.setLayout(HBox)

        self.DialogWin.show()
        QApplication.processEvents()



    # Hata mesajı uyarısı (Kullanıldığı zamanlar : Veri tabanında tablo yoksa, Giriş başarısız ise)
    def errorMessage(self, text = "Incorrect username                   "):
        self.No_Data_Loaded_MsngBox = QMessageBox()
        self.No_Data_Loaded_MsngBox.setIcon(QMessageBox.Warning)
        self.No_Data_Loaded_MsngBox.setWindowTitle("A problem was encountered!")
        self.No_Data_Loaded_MsngBox.setStyleSheet("Background-color: #000229; color: #DBDBDD;")
        self.No_Data_Loaded_MsngBox.setText(text)
        self.No_Data_Loaded_MsngBox.show() 

    # Bilgilendirme mesajı uyarısı (Kullanıldığı zamanlar : Giriş başarılı ise)
    def informationMessage(self):
        self.No_Data_Loaded_MsngBox = QMessageBox()
        self.No_Data_Loaded_MsngBox.setIcon(QMessageBox.Information)
        self.No_Data_Loaded_MsngBox.setStyleSheet("Background-color: #000229; color: #DBDBDD;")
        self.No_Data_Loaded_MsngBox.setText("Login successful    ")
        self.No_Data_Loaded_MsngBox.show() 
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MAIN = Main()
    sys.exit(app.exec_())
    