import sqlite3
import numpy as np

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