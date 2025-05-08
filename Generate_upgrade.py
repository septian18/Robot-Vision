import os

dataname = f'datafile.txt'

def header(folder_path,dataset_name):
    output = f"\n// {dataset_name}\n\n"
    let = process_files_in_folder(output,folder_path, dataset_name)
    return let

def process_file(file_path, dataset_name, dataset_index):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Menghitung jumlah baris dan kolom
    num_rows = len(lines)
    num_cols = len(lines[0].strip()) if num_rows > 0 else 0

    output = f"dataset::{dataset_name}{dataset_index+1} ()\n{{\n"
    output += f"   baris = {num_rows} ;\n"
    output += f"   kolom = {num_cols} ;\n\n"

    # Proses setiap baris seperti sebelumnya
    for idx, line in enumerate(lines):
        line = line.strip()  # Hilangkan spasi atau newline di akhir
        length = len(line)

        count = 0
        current_char = line[0]
        start_idx = 0

        output += f"//baris {idx}\n"

        for i, char in enumerate(line):
            if char == current_char:
                count += 1
            else:
                end_idx = i - 1
                output += f"for (byte i= {start_idx} ;i<= {end_idx} ;i++) {{\n"
                output += f"wajah[ {idx} ][i]= {current_char} ; }}\n"
                start_idx = i
                count = 1
                current_char = char

        # Tambahkan kelompok terakhir
        if count > 0:
            output += f"for (byte i= {start_idx} ;i<= {length - 1} ;i++) {{\n"
            output += f"wajah[ {idx} ][i]= {current_char} ; }}\n\n"

    output += "}\n\n"
    return output


def process_files_in_folder(output,folder_path, dataset_name):
    # Dapatkan semua file .txt dalam folder
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

    all_output = ""
    
    all_output += output
    
    for idx, file_path in enumerate(sorted(file_paths)):
        all_output += process_file(file_path, dataset_name, idx)
    return all_output

# Input nama dasar dataset dari user
dataset_name = input("Masukkan nama dasar untuk dataset: ")
folder_path = input ("Masukkan path: ")
# Proses semua file dalam folder
result = header(folder_path,dataset_name)
print(result)

# Jika ingin menyimpan hasilnya ke file, tambahkan:
output = input ("Nama file output .txt: ")
with open(output, "w") as output_file:
    output_file.write(result)
    
def main(output):
    # Input nama dasar dataset dari user
    dataset_name = input("Masukkan nama dasar untuk dataset: ")
    folder_path = input ("Masukkan path: ")
    # Proses semua file dalam folder
    res = header(folder_path,dataset_name)
    print(res)
    with open (output,"a") as patch:
        patch.write(res)

# nambahin path lain dalam data
while True:
    print("\n1. tambah file")
    print("etc. cetak file\n")
    i = int(input("masukkan menu yang dipilih : "))
    if i == 1:
        main(output)
    else:
        print("terima Kasih !\n")
        break



