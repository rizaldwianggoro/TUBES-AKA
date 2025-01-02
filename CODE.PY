import time
import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from datetime import datetime, timedelta
import sys

# Tingkatkan batas rekursi untuk kebutuhan eksperimen
sys.setrecursionlimit(15000)

def linear_search_iterative(arr, target):
    for i in range(len(arr)):
        if arr[i]['name'] == target:
            return i
    return -1

def linear_search_recursive(arr, target, index=0):
    if index >= len(arr):
        return -1
    if arr[index]['name'] == target:
        return index
    return linear_search_recursive(arr, target, index + 1)

def measure_execution_time(function, arr, target, repetitions=10):
    start_time = time.perf_counter()
    for _ in range(repetitions):
        function(arr, target)
    end_time = time.perf_counter()
    return (end_time - start_time) / repetitions

def check_expired_items(arr):
    today = datetime.now()
    expired_items = [item for item in arr if datetime.strptime(item['expiry_date'], '%Y-%m-%d') < today]
    return expired_items

sizes = []
iterative_times = []
recursive_times = []

def update_graph():
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, iterative_times, label='Iterative', marker='o', linestyle='-')
    if None not in recursive_times:
        plt.plot(sizes, recursive_times, label='Recursive', marker='o', linestyle='-')
    plt.title('Performance Comparison: Linear Search (Iterative vs Recursive)')
    plt.xlabel('Input Size')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

def print_execution_table():
    table = PrettyTable()
    table.field_names = ["Data Size", "Iterative Time (s)", "Recursive Time (s)"]
    for i in range(len(sizes)):
        recursive_time = recursive_times[i] if recursive_times[i] is not None else "Skipped"
        table.add_row([sizes[i], iterative_times[i], recursive_time])
    print(table)

# Program utama
while True:
    try:
        size = int(input("Masukkan ukuran data (atau ketik -1 untuk keluar): "))
        if size == -1:
            print("Program selesai. Terima kasih!")
            break
        if size <= 0:
            print("Masukkan ukuran data yang positif!")
            continue

        # Generate data barang dengan proporsi kedaluwarsa kecil
        arr = [{
            'name': f'Barang-{i+1}',
            'expiry_date': (
                (datetime.now() + timedelta(days=random.randint(-10, 10))).strftime('%Y-%m-%d') 
                if random.random() < 0.1 else  
                (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            )
        } for i in range(size)]
        target = random.choice(arr)['name']

        sizes.append(size)

        # Ukur waktu eksekusi iteratif
        iterative_time = measure_execution_time(linear_search_iterative, arr, target)
        iterative_times.append(iterative_time)

        # Ukur waktu eksekusi rekursif hanya untuk data kecil
        if size <= 15000:
            recursive_time = measure_execution_time(linear_search_recursive, arr, target)
            recursive_times.append(recursive_time)
        else:
            print(f"Ukuran data {size} terlalu besar untuk pengujian rekursi. Hanya iteratif yang diuji.")
            recursive_times.append(None)

        # Tampilkan barang kedaluwarsa
        expired_items = check_expired_items(arr)
        print("\nBarang Kedaluwarsa:")
        if expired_items:
            for item in expired_items:
                print(f"- {item['name']} (Kedaluwarsa pada {item['expiry_date']})")
        else:
            print("Tidak ada barang yang kedaluwarsa.")

        # Cetak tabel waktu eksekusi
        print_execution_table()

        # Perbarui grafik
        update_graph()

    except ValueError:
        print("Masukkan ukuran data yang valid!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
