import serial
import time
import cv2
import os

# Inisialisasi Haar Cascade untuk deteksi wajah
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Membuat direktori penyimpanan gambar dan data jika belum ada
base_folder = 'Captured'
os.makedirs(base_folder, exist_ok=True)
rgb_folder = os.path.join(base_folder, 'RGB')
gray_folder = os.path.join(base_folder, 'Grayscale')
binary_folder = os.path.join(base_folder, 'Binary')
data_folder = os.path.join(base_folder, 'Data')
for folder in [rgb_folder, gray_folder, binary_folder, data_folder]:
    os.makedirs(folder, exist_ok=True)

# Mengatur nama file awal
file_count = 0
rgb_filename = f'img_{file_count}_rgb.jpg'
gray_filename = f'img_{file_count}_gray.jpg'
binary_filename = f'img_{file_count}_binary.jpg'
data_filename = f'data{file_count}.txt'

# Menghubungkan Serial Port (ubah port sesuai konfigurasi Raspberry Pi)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Biasanya Raspberry menggunakan '/dev/ttyUSB0'

try:
    while True:
        # Membaca gambar dari kamera
        ret, img = cap.read()
        if not ret:
            print("Gagal mendapatkan frame dari kamera.")
            break

        # Konversi gambar ke skala abu-abu dan biner
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        # Deteksi wajah dalam gambar skala abu-abu
        faces = face_cascade.detectMultiScale(gray, 1.1, 9)

        for (x, y, w, h) in faces:
            # Panel Normal: Menampilkan bounding box (BB) utama dan koordinatnya
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, f'Main: ({x}, {y})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(img, f'{w} x {h} pixels', (x, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Panel Inner: Area lebih kecil dalam bounding box utama
            inner_x, inner_y, inner_w, inner_h = x + 20, y + 35, w - 40, h - 80
            cv2.rectangle(img, (inner_x, inner_y), (inner_x + inner_w, inner_y + inner_h), (0, 0, 255), 2)
            cv2.putText(img, f'Inner: ({inner_x}, {inner_y})', (inner_x, inner_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            cv2.putText(img, f'{inner_w} x {inner_h} pixels', (inner_x, inner_y + inner_h + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Crop dan ubah bagian inner menjadi binerisasi
            ic = img[y:y + h, x:x + w]
            gc = gray[y:y + h, x:x + w]
            bc = binary[y:y + h, x:x + w]
            data = (bc / 255).astype(int)

            # Kondisi ukuran bounding box untuk penentuan jarak
            if 130 <= w <= 150 and 130 <= h <= 150:
                cv2.putText(img, "in range, keep steady", (10, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Simpan gambar dan data biner
                cv2.imwrite(os.path.join(rgb_folder, rgb_filename), ic)
                cv2.imwrite(os.path.join(gray_folder, gray_filename), gc)
                cv2.imwrite(os.path.join(binary_folder, binary_filename), bc)
                with open(os.path.join(data_folder, data_filename), 'w') as file:
                    for row in data:
                        file.write(''.join(map(str, row)) + '\n')

                # Update nama file untuk penyimpanan berikutnya
                file_count += 1
                rgb_filename = f'img_{file_count}_rgb.jpg'
                gray_filename = f'img_{file_count}_gray.jpg'
                binary_filename = f'img_{file_count}_binary.jpg'
                data_filename = f'data{file_count}.txt'

                # Kirim data ke serial
                ser.write(f'{data_filename}\n'.encode())
                for row in data:
                    ser.write('['.encode() + ''.join(map(str, row)).encode() + ']\n'.encode())
                    time.sleep(0.01)
                ser.write('\n'.encode())

            elif 151 <= w <= 170 and 151 <= h <= 170:
                cv2.putText(img, "don't get close", (10, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 185, 255), 2)
            elif 119 <= w <= 129 and 119 <= h <= 129:
                cv2.putText(img, "you are too far", (10, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 185, 255), 2)
            else:
                cv2.putText(img, "out of range", (10, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Tampilkan hasil deteksi
        cv2.imshow('main', img)
        cv2.imshow('bin', binary)

        # Berhenti jika tombol 'Esc' ditekan
        if cv2.waitKey(30) & 0xFF == 27:
            break

finally:
    # Melepaskan resource
    cap.release()
    ser.close()
    cv2.destroyAllWindows()
