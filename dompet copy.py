# Kelompok Dicont OS (3)
# Anggota 
# Raffael Aldrich Setiawan  (V3423070)
# Raihan Kafi Hufayda       (V3423072)
# Rizqi Andri Wijaya        (V3423077)
# Satria Kusuma Mahardika   (V3423079)
# Veri Tri Ariyanto         (V3423085) 

# Judul aplikasi : DOMPETKU
# sistem untuk mencatat transaksi uang cash dan cashless


import pandas as pd
from tabulate import tabulate
import csv
from datetime import datetime

# Fungsi untuk menambahkan uang cash dan cashless pertama kali
def tambah_uang_pertama_kali():
    cash = float(input("Masukkan jumlah uang cash awal: "))
    cashless = float(input("Masukkan jumlah uang cashless awal: "))
    
    # Menyimpan uang cash dan cashless ke dalam file CSV
    with open("uang.csv", mode='w', newline='') as file: # membuka atau membuat file yang bernama uang.csv , mode 'w' = membuka file dalam mode write (menulis)
        writer = csv.writer(file) # membuat objek penulis yang akan digunakan untuk menulis csv
        writer.writerow(['cash', 'cashless']) # menulis baris pertama dengan cash / cashless
        writer.writerow([cash, cashless]) # menulis baris kedua dngan nilai dari variabel cash / cashless
    
    print("Jumlah uang cash dan cashless telah disimpan.")

# Fungsi untuk menambahkan transaksi
def tambah_transaksi(): 
    tanggal = datetime.now() #mengambil waktu saat ini / realtime
    print("Pilih jenis transaksi:")
    print("1. Pemasukan")
    print("2. Pengeluaran")
    print("3. Pemindahan uang")
    choice = int(input("Masukkan pilihan (1/2/3): ")) # memasukkan input pilihan angka untuk memilih jenis transaksi
    
    if choice == 1: # jika memilih 1 maka proses pemasukan akan dioperasikan 
        kategori, uang, nominal = proses_pemasukan() # return atau pengembalian nilai dari proses pemasukan akan diterima oleh 3 variabel tersebut (kategori, uang, nominal)
    elif choice == 2: # jika memilih 2 maka proses pengeluaran akan dioperasikan
        kategori, uang, nominal = proses_pengeluaran() # return atau pengembalian nilai dari proses pengeluaran akan diterima oleh 3 variabel tersebut (kategori, uang, nominal) 
    elif choice == 3: # jika memilih 3 maka proses pemindahan uang akan dioperasikan 
        kategori, uang, nominal = proses_pemindahan()  # return atau pengembalian nilai dari proses pemindahan akan diterima oleh 3 variabel tersebut (kategori, uang, nominal) 
    else:
        print("Pilihan tidak valid.")

    deskripsi = input("Tambahkan keterangan transaksi: ") # menambahkan deskripsi transaksi 
    transaksi = {
        'tanggal': tanggal,
        'jenis uang': uang,
        'nominal': nominal,
        'kategori': kategori,
        'deskripsi': deskripsi
    }  # data transaksi akan disimpan ke dalam variabel transaksi dan dimasukkan ke dalam tipe data koleksi yaitu dictionary
    print(f"Transaksi telah ditambahkan.")
    simpan_transaksi(transaksi) # data transaksi akan diproses oleh fungsi simpan_transaksi

# Fungsi untuk memproses pemasukan
def proses_pemasukan(): 
    print("Pilih jenis pemasukan:")#user memilih menggunakan jenis uang cash atau cashless
    print("1. Uang cash")
    print("2. Uang cashless")
    jenis_uang = input("Masukkan pilihan (1/2): ")
    if jenis_uang == '1':
        nominal = input_pemasukan("cash") # jika user memilih 1 maka fungsi input_pemasukan memiliki argumen "cash" 
        uang = "cash"
    elif jenis_uang == '2':
        nominal = input_pemasukan("cashless") # jika user memilih 2 maka fungsi input_pemasukan memiliki argumen "cashless"
        uang = "cashless"
    else:
        print("Pilihan tidak valid.")
        return None, None, None
    return "Pemasukan", uang, nominal #fungsi proses_pemasukan ini akan memberikan return "pemasukan" nilai dari variabel uang dan nominal

# Fungsi untuk memproses pengeluaran
def proses_pengeluaran():
    print("Pilih jenis pengeluaran:")
    print("1. Uang cash")
    print("2. Uang cashless")
    jenis_uang = input("Masukkan pilihan (1/2): ")
    if jenis_uang == '1':
        nominal = input_pengeluaran("cash") # jika user memilih 1 maka fungsi input_pengeluaran memiliki argumen "cash" 
        uang = "cash"
    elif jenis_uang == '2':
        nominal = input_pengeluaran("cashless") # jika user memilih 2 maka fungsi input_pengeluaran memiliki argumen "cashless" 
        uang = "cashless"
    else:
        print("Pilihan tidak valid.")
        return None, None, None
    return "Pengeluaran", uang, nominal #fungsi proses_pengeluaran ini akan memberikan return "pemasukan" nilai dari variabel uang dan nominal


# Fungsi untuk memproses pemindahan uang
def proses_pemindahan():
    print("Pilih Perpindahan:")
    print("1. Cash ke Cashless")
    print("2. Cashless ke Cash")
    pindah = input("Masukkan pilihan (1/2): ")
    if pindah == "1":
        dari, ke = "cash", "cashless" #proses perpindahan dari CASH ke CASHLESS
    elif pindah == "2":
        dari, ke = "cashless", "cash" #proses perpindahan dari Cashless ke cash
    else:
        print("Pilihan tidak valid.")
        return None, None, None

    nominal = perpindahan_uang()
    update_uang(dari, -nominal) #uang akan terupdate dengan mengurangi uang dari variabel "dari"
    update_uang(ke, nominal) # akan menambahkan nominal dari variabel  "ke"
    return "Pemindahan", dari, nominal # proses perpindahan uang akan mengembalikan nilai "pemindahan" , dan value dari variabel "dari" dan "ke"

# Fungsi untuk menambahkan pemasukan
def input_pemasukan(jenis): # parameter jenis ini akan sesuai dari pilihan yang kita inputkan dari proses_pemasukan 
    jumlah = float(input("Masukkan jumlah pemasukan: "))
    update_uang(jenis, jumlah) #fungsi update_uang memiliki 2 parameter yaitu jenis dan jumlah sesuai nilai yang kita inputkan
    return jumlah #variabel jumlah di return agar dapat diakses oleh fungsi yang lainnya

# Fungsi untuk menambahkan pengeluaran
def input_pengeluaran(jenis):  # parameter jenis ini akan sesuai dari pilihan yang kita inputkan dari proses_pengeluaran
    jumlah = float(input("Masukkan jumlah pengeluaran: "))
    update_uang(jenis, -jumlah) #fungsi update_uang memiliki 2 parameter yaitu jenis dan jumlah sesuai nilai yang kita inputkan
    return jumlah #variabel jumlah di return agar dapat diakses oleh fungsi yang lainnya

# Fungsi untuk memindahkan uang
def perpindahan_uang(): # fungsi perpindahan_uang bertujuan untuk mengembalikan nilai jumlah dan memberikan input nilai
    jumlah = float(input("Masukkan jumlah uang yang ingin dipindahkan: "))
    return jumlah

# Fungsi untuk mengupdate jumlah uang
def update_uang(jenis, jumlah):
    with open("uang.csv", mode='r') as file: # Membuka file uang.csv dalam mode baca ('r').
        reader = csv.DictReader(file) #Menggunakan csv.DictReader untuk membaca isi file sebagai dictionary.
        row = next(reader)  #Menggunakan csv.DictReader untuk membaca isi file sebagai dictionary.
        cash = float(row['cash']) #Mengambil nilai cash dan cashless dari baris tersebut dan mengonversinya ke tipe float.
        cashless = float(row['cashless'])
    
    if jenis == "cash": #Jika jenis adalah "cash", menambahkan jumlah ke variabel cash.
        cash += jumlah
    elif jenis == "cashless": #Jika jenis adalah "cashless", menambahkan jumlah ke variabel cashless.
        cashless += jumlah
    #Menulis Kembali ke File CSV uang.csv:
    with open("uang.csv", mode='w', newline='') as file: #Membuka file uang.csv dalam mode tulis ('w') atau writter
        writer = csv.writer(file) #Menggunakan csv.writer untuk menulis ke file.
        writer.writerow(['cash', 'cashless']) #Menulis header ('cash', 'cashless') ke file.
        writer.writerow([cash, cashless]) #Menulis nilai cash dan cashless yang sudah diperbarui ke file.
    
    print(f"Jumlah uang {jenis} telah diupdate. Jumlah sekarang: {cash if jenis == 'cash' else cashless}")

# Fungsi untuk memeriksa apakah file uang.csv sudah ada atau belum
def cek_file_ada():
    try:
        with open("uang.csv", mode='r') as file: #Fungsi ini mencoba membuka file uang.csv dalam mode baca ('r').
            return True # Jika file berhasil dibuka, fungsi akan mengembalikan nilai True, menandakan bahwa file tersebut ada.
    except FileNotFoundError: #Jika file uang.csv tidak ditemukan, akan muncul kesalahan FileNotFoundError.
        return False #Kesalahan ini ditangkap oleh blok except, dan fungsi mengembalikan nilai False, menandakan bahwa file tersebut tidak ada.

# Fungsi untuk melihat saldo
def lihat_saldo(): 
    df = pd.read_csv('uang.csv') #dengan menggunakan library pandas untuk membaca file csv dan memasukkannya kedalam variabel df 
    table = tabulate(df, headers='keys', tablefmt='pretty') #menggunakan library tabulate untuk membuat border dari hasil baca file csv menggunakan pandas
    print(table)

# Fungsi untuk menyimpan transaksi ke file CSV
def simpan_transaksi(transaksi):
    filename = "mutasi.csv"
    with open(filename, 'a', newline='') as csvfile: #Menggunakan statement with open(...) untuk membuka file CSV dengan mode 'a' (append). Mode 'a' digunakan agar data baru dapat ditambahkan ke file tanpa menghapus data yang sudah ada.
        fieldnames = ('tanggal', 'jenis uang', 'nominal', 'kategori', 'deskripsi') #fieldnames adalah tuple yang berisi nama-nama kolom (header) yang akan digunakan dalam file CSV. Kolom-kolom ini sesuai dengan kunci-kunci yang ada dalam dictionary transaksi.
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) #csv.DictWriter digunakan untuk menulis baris-baris data ke file CSV berdasarkan dictionary. writer adalah objek yang bertanggung jawab untuk menulis data ke file CSV yang telah dibuka (csvfile).

        # Menulis header hanya jika file masih kosong
        if csvfile.tell() == 0: #csvfile.tell() digunakan untuk mendapatkan posisi (offset) saat ini dalam file. Jika posisi tersebut adalah 0, berarti file masih kosong.
            writer.writeheader()

        writer.writerow(transaksi) #writer.writerow(transaksi) digunakan untuk menulis satu baris data transaksi ke file CSV. Parameter transaksi adalah dictionary yang berisi informasi tentang satu transaksi.
    print(f"Informasi transaksi telah disimpan ke file '{filename}'.")

def mutasi():
    print("Melihat berdasarkan : ")
    print("1. Kategori Transaksi")
    print("2. Jenis Uang")
    print("3. Tanggal")
    print("4. Semuanya")
    sort = int(input("Pilih (1/4) : "))
    #memilih melihat mutasi berdasarkan apa, 
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
    #Memisahkan data berdasarkan nilai kategori menggunakan conditional indexing pada dataframe df. pemasukan, pengeluaran, dan pemindahan akan berisi subset dari dataframe df yang hanya berisi transaksi dengan kategori masing-masing 'Pemasukan', 'Pengeluaran', dan 'Pemindahan'.
    pemasukan = df[df['kategori'] == 'Pemasukan']
    pengeluaran = df[df['kategori'] == 'Pengeluaran']
    pemindahan = df[df['kategori'] == 'Pemindahan']


    #Menggunakan fungsi tabulate untuk mengonversi dataframe pemasukan, pengeluaran, dan pemindahan menjadi tabel dengan format yang lebih rapi. Parameter headers='keys' digunakan untuk menampilkan header (nama kolom) dari dataframe sebagai bagian atas tabel, dan tablefmt='pretty' digunakan untuk mendapatkan output yang lebih terstruktur dan mudah dibaca.
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
    #Menggunakan pd.read_csv() dari library pandas (import pandas as pd) untuk membaca file CSV yang bernama 'mutasi.csv' dan memuatnya ke dalam dataframe df.
    df = pd.read_csv('mutasi.csv')

    #Memisahkan data berdasarkan nilai kolom 'jenis uang'. cash akan berisi subset dari dataframe df yang hanya berisi transaksi dengan jenis uang 'cash', sedangkan cashless akan berisi transaksi dengan jenis uang 'cashless'.
    cash = df[df['jenis uang'] == 'cash']
    cashless = df[df['jenis uang'] == 'cashless']


    #Menggunakan fungsi tabulate untuk mengonversi dataframe cash dan cashless menjadi tabel dengan format yang lebih rapi. Parameter headers='keys' digunakan untuk menampilkan header (nama kolom) dari dataframe sebagai bagian atas tabel, dan tablefmt='pretty' digunakan untuk mendapatkan output yang lebih terstruktur dan mudah dibaca.
    table_cash = tabulate(cash, headers='keys', tablefmt='pretty')
    table_cashless = tabulate(cashless, headers='keys', tablefmt='pretty')
    print("\n============== CASH ==============")
    print(table_cash)
    print("\n============== CASHLESS ==============")
    print(table_cashless)

def sort_tanggal():
    #Fungsi ini meminta pengguna untuk memasukkan tahun dan bulan dalam bentuk angka menggunakan fungsi input(). Angka-angka ini kemudian dikonversi menjadi tipe data integer (int).
    tahun = int(input("Masukkan tahun: "))
    bulan = int(input("Masukkan bulan (1-12): "))
    tanggal = int(input("Masukkan tanggal: "))

    df = pd.read_csv('mutasi.csv')
    df['tanggal'] = pd.to_datetime(df['tanggal'])  # Konversi kolom 'tanggal' ke datetime
    
    # Filter berdasarkan bulan, tanggal, dan tahun
    df_tanggal = df[(df['tanggal'].dt.year == tahun) &
                    (df['tanggal'].dt.month == bulan) &
                    (df['tanggal'].dt.day == tanggal)]
    #if not df_tanggal.empty = jika data kosong == false (yang artinya ada datanya maka menampilkan data)
    if not df_tanggal.empty: # jika ada transaksi di tanggal bulan dan tahun tersebut maka akan menampilkan data
        table = tabulate(df_tanggal, headers='keys', tablefmt='pretty')
        print("\nData transaksi untuk tanggal {}-{}-{}:".format(tahun, bulan, tanggal))
        print(table)
    else: #jika tidak ada maka akan menampilkan ini diconsole
        print("\nTidak ada data transaksi untuk tanggal {}-{}-{}.".format(tahun, bulan, tanggal))

def sort_all():
    #menampilkan seluruh riwayat transaksi 
    df = pd.read_csv('mutasi.csv')
    table = tabulate(df, headers='keys', tablefmt='pretty')
    print(table)

# Fungsi utama
def utama():
    if not cek_file_ada(): #melakukan pengecekan dengan fungsi cek_file_ada, jka hasil return false maka fungsi tambah_uang_pertama_kali akan dijalankan
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
