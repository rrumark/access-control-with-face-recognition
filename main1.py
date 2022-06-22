from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


import sys


import cv2
import face_recognition
import numpy as np
import sqlite3


class Database:
    # Burada kullanıcı görselini (x, y, z) boyutundan (m, n) boyutuna çeviriyoruz.
    # Bu işlemi (R, G, B) kodlarını tek bir değer olarak alıp string veri tipine çevirerek yapıyoruz.
    # Böylece kullanıcı göresli veri tabanına aktarmaya uygun hala getiriyoruz.
    def get3Dto2D(self, img): 
        
        Data = list()
        
        for i in range(len(img)):
            
            templist = list()
            for j in range(len(img[i])):
                temp = str(img[i][j][0]) + "-" + str(img[i][j][1]) + "-" + str(img[i][j][2])
                templist.append(temp)
            
            Data.append(templist)
        
        return Data

    # Kullanıcı göreslini uygun hale getirdikten sonra, tablo ismi ve görsel data veri tabanına aktarılıyor.
    # Burada tablo ismi aynı zamanda username olmaktadır. 
    def createTable(self, tableName, veri): 
        try:
            columnsSize = len(veri)
            columnNames = ""
            for i in range(columnsSize): # Veri tabını tablo sütun isimlerinin oluşturulması : (0, 1, 2, 3, ...) --> (_0, _1, _2, ...)
                columnNames += "{} STRING, ".format("_" + str(i))
            
            
            connect = sqlite3.connect("DatabaseLoginVideo.db")
            cur = connect.cursor()
            
            cur.execute("""CREATE TABLE {} ({})""".format(tableName, columnNames[:-2]))
            

            for i in range(len(veri[0])): # Tabloda ki her satır tek tek tabloya eklemek için düzenleniyor.
                row = ""
                for j in range(len(veri)):
                    row += "'{}',".format(veri[j][i])
                
                cur.execute("INSERT INTO {} VALUES ({})".format(tableName, row[:-1])) # Düzenlenen satırlar tabloya ekleniyor.
                    
            connect.commit()
            connect.close()

            return True # Eğer ekleme başarılı ise True değeri döndürüyor.
        except:
            return False # Eğer ekleme başarısız ise False değeri döndürüyor.

    # username (tablo ismi) 'i parametre alarak veri tabanında o tablo mevcut ise tabloyu çeker ve tablo yu döndürür.
    # Eğer mevcut değilse False değerini döndürür.
    def databaseExtraction(self, tableName): 
        try:
            con = sqlite3.connect("DatabaseLoginVideo.db")
            cur = con.cursor()
                    
            columnNames = list(map(lambda x: x[0], cur.execute("SELECT * FROM {}".format(tableName)).description)) # Tabloda ki sürun isimlerini çeker
            
            valList = list()
            for i, j in enumerate(columnNames): # Sırayla sütunda ki verileri çeker bir listeye atar.
                data = cur.execute("SELECT {} FROM {}".format(j, tableName))
                        
                array = list()
                for i in data:
                    array.append(i[0])
                
                valList.append(array) # Litenin son hali
                
            con.commit()
            con.close()

            return valList
        except:
            return False

    
    # Veri tabanından çekilen veriler tekrardan yüz karşılaştırma işlemlerine uygun formata çevirmek için. (np.array, unit8)
    def get2Dto3D(self, Data): 
        
        lastList = list()
        for i in Data:
            tempList = list()
            
            for ind in range(len(i)):
                row = i[ind].split("-")
                
                for _ in range(len(row)):
                    row[_] = int(row[_])
                    
                tempList.append(row)
                
            lastList.append(tempList)
                
        array = np.array(lastList, dtype = "uint8")

        return array

class videLogin:
    # İçerisine aldığı iki fotoğraf değerini birbiri ile karşılaştırır.
    # Eğer fotoğraftaki kişiler belli bir benzerlik oranında ise True, değilse False döndürür.
    def photoComparison(self, img1, img2): 
        
        img_1 = face_recognition.face_encodings(img1)[0]
        img_2 = face_recognition.face_encodings(img2)[0]
        
        results = face_recognition.compare_faces([img_1], img_2)

        return results
     
    # Video penceresini açar ve 'R' ya da 'r' tuşlarına basıldığı anda parametre olarak aldığı
    # image (Veri tabanında ki kullanıcı görseli) self.photoComparison fonksiynu yardıymıyla video penceresinden
    # aldığı görselleri karşılaştırır. E
    # Eğer eşlemek doğru ise self.statu değişkeni True değeri, yanlış ise False değeri atar.
    def showVideo(self, image): 
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        while(True):
            ret, frame = vid.read()
            cv2.imshow("Press 'R' to login.", frame)
            
            if cv2.waitKey(1) & 0xFF in [ord('R'), ord('r')]:
                
                try:
                    result = self.photoComparison(frame, image) # Karşılaştırma 
                except:
                    result = [False]

                if result[0]:
                    self.statu = True
                    break
                else:
                    self.statu = False
                    break
        
        vid.release()
        cv2.destroyAllWindows()


    # Bu fonksiyon daha sonra araytüz sınıfında fotoğraf eşleştirme sonucunun ne olduğu görmek içindir.
    def getStatu(self): 

        return self.statu




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
        self.pixmap = QPixmap('login.png')
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
        self.setStyleSheet("QMainWindow {background-image : url(back.jpg);}") 

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
    