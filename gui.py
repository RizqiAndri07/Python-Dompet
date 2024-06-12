import sys
import csv
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTextEdit, QMessageBox
)

transactions = []

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Manajemen Keuangan")

        layout = QVBoxLayout()

        self.label = QLabel("Pilih tindakan:")
        layout.addWidget(self.label)

        self.buttonTambah = QPushButton("Tambah Transaksi")
        self.buttonTambah.clicked.connect(self.tambahTransaksi)
        layout.addWidget(self.buttonTambah)

        self.buttonLihat = QPushButton("Lihat Saldo")
        self.buttonLihat.clicked.connect(self.lihatSaldo)
        layout.addWidget(self.buttonLihat)

        self.setLayout(layout)

    def tambahTransaksi(self):
        self.tambahTransaksiWindow = TambahTransaksiWindow()
        self.tambahTransaksiWindow.show()

    def lihatSaldo(self):
        lihat_saldo()

class TambahTransaksiWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tambah Transaksi")

        layout = QVBoxLayout()

        self.labelJenis = QLabel("Pilih jenis transaksi:")
        layout.addWidget(self.labelJenis)

        self.comboBoxJenis = QComboBox()
        self.comboBoxJenis.addItems(["Pemasukan", "Pengeluaran", "Pemindahan uang"])
        layout.addWidget(self.comboBoxJenis)

        self.comboBoxJenis.currentIndexChanged.connect(self.updateJenisTransaksi)

        self.labelJenisUang = QLabel("Pilih jenis uang:")
        layout.addWidget(self.labelJenisUang)

        self.comboBoxJenisUang = QComboBox()
        self.comboBoxJenisUang.addItems(["Uang cash", "Uang cashless"])
        layout.addWidget(self.comboBoxJenisUang)

        self.labelJumlah = QLabel("Masukkan jumlah:")
        layout.addWidget(self.labelJumlah)

        self.inputJumlah = QLineEdit()
        layout.addWidget(self.inputJumlah)

        self.labelDeskripsi = QLabel("Tambahkan keterangan transaksi:")
        layout.addWidget(self.labelDeskripsi)

        self.inputDeskripsi = QTextEdit()
        layout.addWidget(self.inputDeskripsi)

        self.buttonSimpan = QPushButton("Simpan")
        self.buttonSimpan.clicked.connect(self.simpanTransaksi)
        layout.addWidget(self.buttonSimpan)

        self.setLayout(layout)

    def updateJenisTransaksi(self):
        jenis = self.comboBoxJenis.currentText()
        if jenis == "Pemindahan uang":
            self.comboBoxJenisUang.hide()
            self.labelJenisUang.hide()
        else:
            self.comboBoxJenisUang.show()
            self.labelJenisUang.show()

    def simpanTransaksi(self):
        jenis_transaksi = self.comboBoxJenis.currentText()
        jenis_uang = self.comboBoxJenisUang.currentText()
        nominal = float(self.inputJumlah.text())
        deskripsi = self.inputDeskripsi.toPlainText()

        tanggal = datetime.now()

        if jenis_transaksi == "Pemasukan":
            kategori, uang, nominal = "Pemasukan", jenis_uang, nominal
            if jenis_uang == "Uang cash":
                update_uang("cash", nominal)
                uang = "cash"
            elif jenis_uang == "Uang cashless":
                update_uang("cashless", nominal)
                uang = "cashless"
        elif jenis_transaksi == "Pengeluaran":
            kategori, uang, nominal = "Pengeluaran", jenis_uang, nominal
            if jenis_uang == "Uang cash":
                update_uang("cash", -nominal)
                uang = "cash"
            elif jenis_uang == "Uang cashless":
                update_uang("cashless", -nominal)
                uang = "cashless"
        elif jenis_transaksi == "Pemindahan uang":
            jumlah = perpindahan_uang()
            update_uang("cash", -jumlah)
            update_uang("cashless", jumlah)
            kategori, uang, nominal = "Pemindahan", "cash", jumlah

        transaksi = {
            'tanggal': tanggal,
            'jenis uang': uang,
            'nominal': nominal,
            'jenis transaksi': kategori,
            'deskripsi': deskripsi
        }
        transactions.append(transaksi)
        simpan_transaksi(transaksi)
        QMessageBox.information(self, "Informasi", "Transaksi telah disimpan")

def tambah_uang_pertama_kali():
    cash = float(input("Masukkan jumlah uang cash awal: "))
    cashless = float(input("Masukkan jumlah uang cashless awal: "))

    with open("uang.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['cash', 'cashless'])
        writer.writerow([cash, cashless])

    print("Jumlah uang cash dan cashless telah disimpan.")

def update_uang(jenis, jumlah):
    try:
        with open("uang.csv", mode='r') as file:
            reader = csv.DictReader(file)
            row = next(reader)
            cash = float(row['cash'])
            cashless = float(row['cashless'])

        if jenis == "cash":
            cash += jumlah
        elif jenis == "cashless":
            cashless += jumlah

        with open("uang.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['cash', 'cashless'])
            writer.writerow([cash, cashless])

        print(f"Jumlah uang {jenis} telah diupdate. Jumlah sekarang: {cash if jenis == 'cash' else cashless}")
    except FileNotFoundError:
        tambah_uang_pertama_kali()

def lihat_saldo():
    try:
        with open("uang.csv", mode='r') as file:
            reader = csv.DictReader(file)
            row = next(reader)
            cash = float(row['cash'])
            cashless = float(row['cashless'])

        msg = f"Saldo Cash: {cash}\nSaldo Cashless: {cashless}"
        QMessageBox.information(None, "Saldo", msg)
    except FileNotFoundError:
        QMessageBox.warning(None, "Peringatan", "File uang.csv tidak ditemukan")

def simpan_transaksi(transaksi):
    filename = "mutasi.csv"
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['tanggal', 'jenis uang', 'nominal', 'jenis transaksi', 'deskripsi']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(transaksi)
    print(f"Informasi transaksi telah disimpan ke file '{filename}'.")

def perpindahan_uang():
    jumlah = float(input("Masukkan jumlah yang ingin dipindahkan: "))
    return jumlah

def main():
    if not cek_file_ada():
        tambah_uang_pertama_kali()

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

def cek_file_ada():
    try:
        with open("uang.csv", mode='r') as file:
            return True
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    main()
