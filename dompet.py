import pandas as pd
from tabulate import tabulate
import csv
from datetime import datetime

# Inisialisasi list transaksi
transactions = []

# Fungsi untuk menambahkan uang cash dan cashless pertama kali
def tambah_uang_pertama_kali():
    cash = float(input("Masukkan jumlah uang cash awal: "))
    cashless = float(input("Masukkan jumlah uang cashless awal: "))
    
    # Menyimpan uang cash dan cashless ke dalam file CSV
    with open("uang.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['cash', 'cashless'])
        writer.writerow([cash, cashless])
    
    print("Jumlah uang cash dan cashless telah disimpan.")

# Fungsi untuk menambahkan transaksi
def tambah_transaksi():
    tanggal = datetime.now() #mengambil waktu saat ini / realtime
    print("Pilih jenis transaksi:")
    print("1. Pemasukan")
    print("2. Pengeluaran")
    print("3. Pemindahan uang")
    choice = input("Masukkan pilihan (1/2/3): ")
    
    if choice == '1':
        kategori, uang, nominal = proses_pemasukan()
    elif choice == '2':
        kategori, uang, nominal = proses_pengeluaran()
    elif choice == '3':
        kategori, uang, nominal = proses_pemindahan()
    else:
        print("Pilihan tidak valid.")
        return

    deskripsi = input("Tambahkan keterangan transaksi: ")
    transaksi = {
        'tanggal': tanggal,
        'jenis uang': uang,
        'nominal': nominal,
        'kategori': kategori,
        'deskripsi': deskripsi
    }
    transactions.append(transaksi)
    print(f"Transaksi telah ditambahkan.")
    simpan_transaksi(transaksi)

# Fungsi untuk memproses pemasukan
def proses_pemasukan():
    print("Pilih jenis pemasukan:")
    print("1. Uang cash")
    print("2. Uang cashless")
    jenis_uang = input("Masukkan pilihan (1/2): ")
    if jenis_uang == '1':
        nominal = tambah_pemasukan("cash")
        uang = "cash"
    elif jenis_uang == '2':
        nominal = tambah_pemasukan("cashless")
        uang = "cashless"
    else:
        print("Pilihan tidak valid.")
        return None, None, None
    return "Pemasukan", uang, nominal

# Fungsi untuk memproses pengeluaran
def proses_pengeluaran():
    print("Pilih jenis pengeluaran:")
    print("1. Uang cash")
    print("2. Uang cashless")
    jenis_uang = input("Masukkan pilihan (1/2): ")
    if jenis_uang == '1':
        nominal = tambah_pengeluaran("cash")
        uang = "cash"
    elif jenis_uang == '2':
        nominal = tambah_pengeluaran("cashless")
        uang = "cashless"
    else:
        print("Pilihan tidak valid.")
        return None, None, None
    return "Pengeluaran", uang, nominal

# Fungsi untuk memproses pemindahan uang
def proses_pemindahan():
    print("Pilih Perpindahan:")
    print("1. Cash ke Cashless")
    print("2. Cashless ke Cash")
    pindah = input("Masukkan pilihan (1/2): ")
    if pindah == "1":
        dari, ke = "cash", "cashless"
    elif pindah == "2":
        dari, ke = "cashless", "cash"
    else:
        print("Pilihan tidak valid.")
        return None, None, None

    nominal = perpindahan_uang()
    update_uang(dari, -nominal)
    update_uang(ke, nominal)
    return "Pemindahan", dari, nominal

# Fungsi untuk menambahkan pemasukan
def tambah_pemasukan(jenis):
    jumlah = float(input("Masukkan jumlah pemasukan: "))
    update_uang(jenis, jumlah)
    return jumlah

# Fungsi untuk menambahkan pengeluaran
def tambah_pengeluaran(jenis):
    jumlah = float(input("Masukkan jumlah pengeluaran: "))
    update_uang(jenis, -jumlah)
    return jumlah

# Fungsi untuk memindahkan uang
def perpindahan_uang():
    jumlah = float(input("Masukkan jumlah uang yang ingin dipindahkan: "))
    return jumlah

# Fungsi untuk mengupdate jumlah uang
def update_uang(jenis, jumlah):
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

# Fungsi untuk memeriksa apakah file uang.csv sudah ada atau belum
def cek_file_ada():
    try:
        with open("uang.csv", mode='r') as file:
            return True
    except FileNotFoundError:
        return False

# Fungsi untuk melihat saldo
def lihat_saldo():
    df = pd.read_csv('uang.csv')
    table = tabulate(df, headers='keys', tablefmt='pretty')
    print(table)

# Fungsi untuk menyimpan transaksi ke file CSV
def simpan_transaksi(transaksi):
    filename = "mutasi.csv"
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['tanggal', 'jenis uang', 'nominal', 'kategori', 'deskripsi']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Menulis header hanya jika file masih kosong
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(transaksi)
    print(f"Informasi transaksi telah disimpan ke file '{filename}'.")

def mutasi():
    print("Melihat berdasarkan : ")
    print("1. Kategori Transaksi")
    print("2. Jenis Uang")
    print("3. Tanggal")
    print("4. Semuanya")
    sort = int(input("Pilih (1/4) : "))
    
    if sort == 1:
        sort_jenistransaksi()
    elif sort == 2:
        sort_jenisuang()
    elif sort == 3:
        sort_tanggal()
    elif sort == 4:
        sort_all()
    else:
        print ("Input Tidak valid !")

# filter mutasi
def sort_jenistransaksi():
    df = pd.read_csv('mutasi.csv')
    print("Kolom yang tersedia:", df.columns.tolist())  # Debug: cek kolom yang tersedia
    pemasukan = df[df['kategori'] == 'Pemasukan']
    pengeluaran = df[df['kategori'] == 'Pengeluaran']
    pemindahan = df[df['kategori'] == 'Pemindahan']
    table_pemasukan = tabulate(pemasukan, headers='keys', tablefmt='pretty')
    table_pengeluaran = tabulate(pengeluaran, headers='keys', tablefmt='pretty')
    table_pemindahan = tabulate(pemindahan, headers='keys', tablefmt='pretty')
    print("\n============== PEMASUKAN ==============")
    print(table_pemasukan)
    print("\n============== PENGELUARAN ==============")
    print(table_pengeluaran)
    print("\n============== PEMINDAHAN ==============")
    print(table_pemindahan)

def sort_jenisuang():
    df = pd.read_csv('mutasi.csv')
    cash = df[df['jenis uang'] == 'cash']
    cashless = df[df['jenis uang'] == 'cashless']
    table_cash = tabulate(cash, headers='keys', tablefmt='pretty')
    table_cashless = tabulate(cashless, headers='keys', tablefmt='pretty')
    print("\n============== CASH ==============")
    print(table_cash)
    print("\n============== CASHLESS ==============")
    print(table_cashless)

def sort_tanggal():
    tahun = int(input("masukkan tahun : "))
    bulan = int(input("masukkan bulan : "))
    df = pd.read_csv('mutasi.csv')
    df['tanggal'] = pd.to_datetime(df['tanggal'])  # Konversi kolom 'tanggal' ke datetime
    
    # Filter untuk transaksi pada Mei 2024
    df_tanggal = df[(df['tanggal'].dt.year == tahun) & (df['tanggal'].dt.month == bulan)]
    
    table = tabulate(df_tanggal, headers='keys', tablefmt='pretty')
    print(table)

def sort_all():
    df = pd.read_csv('mutasi.csv')
    table = tabulate(df, headers='keys', tablefmt='pretty')
    print(table)

# Fungsi utama
def utama():
    if not cek_file_ada():
        tambah_uang_pertama_kali()
    
    while True:
        print("\nPilihan:")
        print("1. Tambah Transaksi")
        print("2. Lihat Saldo")
        print("3. Lihat Mutasi")
        print("0. Keluar")
        pilihan = input("Masukkan pilihan (1/2/3/0): ")
        
        if pilihan == '1':
            tambah_transaksi()
        elif pilihan == '2':
            lihat_saldo()
        elif pilihan == '3':
            mutasi()
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    utama()
