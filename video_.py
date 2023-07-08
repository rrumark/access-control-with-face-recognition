import face_recognition
import cv2

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


