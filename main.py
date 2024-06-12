import pandas as pd
from datetime import datetime
import csv

# Daftar transaksi
transactions = []


def add_transaction(date, amount, category, description):
    transaction = {
        'date': date,
        'amount': amount,
        'category': category,
        'description': description
    }
    transactions.append(transaction)
    print(f"Transaksi '{description}' telah ditambahkan.")
    
    # Menyimpan transaksi ke file CSV
    filename = "transactions.csv"
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['date', 'amount', 'category', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Menulis header hanya jika file masih kosong
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(transaction)
    print(f"Informasi transaksi telah disimpan ke file '{filename}'.")


def view_transactions():
    if not transactions:
        print("Tidak ada transaksi dalam sistem.")
    else:
        for index, transaction in enumerate(transactions, start=1):
            print(f"{index}. {transaction['date']} - {transaction['description']} sebesar {transaction['amount']} dalam kategori {transaction['category']}")

def search_transactions_by_category(category):
    found_transactions = [transaction for transaction in transactions if transaction['category'].lower() == category.lower()]
    if not found_transactions:
        print(f"Tidak ada transaksi ditemukan dalam kategori '{category}'.")
    else:
        for transaction in found_transactions:
            print(f"{transaction['date']} - {transaction['description']} sebesar {transaction['amount']}")

def search_transactions_by_date(date):
    found_transactions = [transaction for transaction in transactions if transaction['date'] == date]
    if not found_transactions:
        print(f"Tidak ada transaksi ditemukan pada tanggal '{date}'.")
    else:
        for transaction in found_transactions:
            print(f"{transaction['date']} - {transaction['description']} sebesar {transaction['amount']} dalam kategori {transaction['category']}")

def save_transactions_to_file(filename):
    df = pd.DataFrame(transactions)
    df.to_csv(filename, index=False)
    print(f"Daftar transaksi telah disimpan ke file '{filename}'.")

def load_transactions_from_file(filename):
    try:
        df = pd.read_csv(filename)
        global transactions
        transactions = df.to_dict('records')
        print(f"Daftar transaksi telah dimuat dari file '{filename}'.")
    except FileNotFoundError:
        print(f"File '{filename}' tidak ditemukan.")

def main():
    while True:
        print("\nMenu:")
        print("1. Tambah Transaksi")
        print("2. Lihat Daftar Transaksi")
        print("3. Cari Transaksi Berdasarkan Kategori")
        print("4. Cari Transaksi Berdasarkan Tanggal")
        print("5. Simpan Daftar Transaksi ke File")
        print("6. Muat Daftar Transaksi dari File")
        print("7. Keluar")
        
        choice = input("Pilih opsi (1-7): ")
        
        if choice == '1':
            date = input("Masukkan tanggal transaksi (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("Format tanggal tidak valid.")
                continue
            amount = float(input("Masukkan jumlah transaksi: "))
            category = input("Masukkan kategori transaksi: ")
            description = input("Masukkan deskripsi transaksi: ")
            add_transaction(date, amount, category, description)
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            category = input("Masukkan kategori: ")
            search_transactions_by_category(category)
        elif choice == '4':
            date = input("Masukkan tanggal (YYYY-MM-DD): ")
            search_transactions_by_date(date)
        elif choice == '5':
            filename = input("Masukkan nama file untuk menyimpan: ")
            save_transactions_to_file(filename)
        elif choice == '6':
            filename = input("Masukkan nama file untuk memuat: ")
            load_transactions_from_file(filename)
        elif choice == '7':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
