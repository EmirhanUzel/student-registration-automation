import sys
from PyQt5 import QtWidgets as qtw
from ornek import Ui_MainWindow
from PyQt5.QtWidgets import QTableWidgetItem
import mysql.connector
db=mysql.connector.connect(

)

class Uygulama(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.dogumyer.addItems(["Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"])
        self.ui.kayitekle.clicked.connect(self.kayitekle)
        self.ui.kayitsil.clicked.connect(self.kayitsil)

        self.verilerigetir()
    def verilerigetir(self):
        try:    
            yeni=db.cursor()
            sorgu=("Select * from ogrenciler.bilgiler")
            yeni.execute(sorgu)
            veriler=yeni.fetchall()
            yeni.close()
            self.ui.tableWidget.setRowCount(0)
            for satir_index, satir in enumerate(veriler):
                self.ui.tableWidget.insertRow(satir_index)
                for sutun_index, veri in enumerate(satir):
                    self.ui.tableWidget.setItem(satir_index, sutun_index, QTableWidgetItem(str(veri)))

        except Exception as e:
            qtw.QMessageBox.critical(self, "Hata", f"Veriler getirilirken hata oluştu: {str(e)}")
    def kayitekle(self):

        ad=self.ui.ad.text()
        soyad=self.ui.soyad.text()
        tc=self.ui.tc.text()
        telefon=self.ui.telefon.text()

        cinsiyetgrup=self.ui.cinsiyet.findChildren(qtw.QRadioButton)
        for i in cinsiyetgrup:
            if i.isChecked():
                cinsiyet=i.text()
                break

        dogumyer=self.ui.dogumyer.currentText()
        bolum=self.ui.bolum.currentText()
        dtarih=self.ui.dogumyili.selectedDate()
        dtarih=dtarih.toString("dd-MM-yyyy")

        satirsayisi=self.ui.tableWidget.rowCount()-1
        self.ui.tableWidget.setItem(satirsayisi,0,QTableWidgetItem(ad))
        self.ui.tableWidget.setItem(satirsayisi,1,QTableWidgetItem(soyad))
        self.ui.tableWidget.setItem(satirsayisi,2,QTableWidgetItem(tc))
        self.ui.tableWidget.setItem(satirsayisi,3,QTableWidgetItem(telefon))
        self.ui.tableWidget.setItem(satirsayisi,4,QTableWidgetItem(dtarih))
        self.ui.tableWidget.setItem(satirsayisi,5,QTableWidgetItem(dogumyer))
        self.ui.tableWidget.setItem(satirsayisi,6,QTableWidgetItem(bolum))
        self.ui.tableWidget.setItem(satirsayisi,7,QTableWidgetItem(cinsiyet))

        self.ui.tableWidget.insertRow(satirsayisi+1)

        try:
                yeni = db.cursor()
                sorgu = "INSERT INTO bilgiler (Adı, Soyadı, Tc, Telefon, Dogumtarihi, Dogumyeri, Bolumu, Cinsiyeti) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                yeni.execute(sorgu, (ad, soyad, tc, telefon, dtarih, dogumyer, bolum, cinsiyet))
                db.commit()
                yeni.close()
                qtw.QMessageBox.information(self, "Başarılı", "Kayıt başarıyla eklendi!")
        except Exception as e:
                qtw.QMessageBox.critical(self, "Hata", f"Kayıt eklenirken hata oluştu: {str(e)}")

        self.verilerigetir()
    def kayitsil(self):
        secilisatir=self.ui.tableWidget.currentRow()
        if secilisatir == -1:  
            qtw.QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir kayıt seçin!")
            return

        self.ui.tableWidget.removeRow(secilisatir)
        tc_item=self.ui.tableWidget.item(secilisatir,2)
        tc=tc_item.text()


        try:
            yeni = db.cursor()
            sorgu = "DELETE FROM bilgiler WHERE Tc = %s"
            yeni.execute(sorgu, (tc,))
            db.commit()
            yeni.close()
            qtw.QMessageBox.information(self, "Başarılı", "Kayıt başarıyla silindi!")
        except Exception as e:
            qtw.QMessageBox.critical(self, "Hata", f"Kayıt silinirken hata oluştu: {str(e)}")

def app():
    app=qtw.QApplication(sys.argv)
    win=Uygulama()
    win.show()
    sys.exit(app.exec_())
app()