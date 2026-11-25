# Design Brief - Equipment Loan API

Tugas Individu Komputasi Awan, Week 12 - Design & AWS Setup
Nama: Gilbert S. H. Nainggolan

## 1. Use case
Sistem peminjaman alat untuk mencatat alat yang tersedia, siapa yang
meminjam, dan kapan alat harus dikembalikan. Pengguna dapat menambah alat,
melihat daftar dan detail alat, memperbarui status peminjaman, serta
menghapus alat yang tidak dipakai lagi.

## 2. Track yang dipilih
Track C - Serverless: Lambda Function URL + AWS Lambda + Amazon S3.

Alasan pemilihan:
- Data hanya satu entitas tanpa relasi kompleks, sehingga cukup disimpan
  sebagai objek JSON.
- Tidak perlu mengelola server maupun jaringan (VPC).
- Biaya mengikuti pemakaian, sehingga hemat untuk budget Learner Lab
  yang tidak dapat di-reset.

### Perubahan desain
Rancangan awal memakai API Gateway dan DynamoDB. Kedua layanan itu tidak
tersedia di sandbox AWS yang digunakan, sehingga diganti dengan Lambda
Function URL (endpoint HTTPS) dan S3 (penyimpanan data). Entitas dan
endpoint CRUD tidak berubah.

## 3. Entitas data
Equipment, disimpan sebagai objek JSON di S3 dengan key `equipment/{id}.json`.

| Atribut | Tipe | Keterangan |
|---|---|---|
| id | String | Pengenal unik, contoh: eq-001 (menjadi nama objek) |
| name | String | Nama alat |
| category | String | Kategori alat |
| status | String | available / borrowed |
| borrower | String | Nama peminjam (kosong jika tersedia) |
| borrowed_at | String | Tanggal pinjam |
| due_date | String | Batas tanggal kembali |

## 4. Endpoint CRUD
Function URL hanya satu alamat, sehingga pemilihan operasi dilakukan di
dalam kode Lambda berdasarkan method dan path.

| Operasi | Method | Path | Fungsi |
|---|---|---|---|
| Create | POST | /equipment | Menambah alat baru |
| Read | GET | /equipment, /equipment/{id} | Daftar atau detail alat |
| Update | PUT | /equipment/{id} | Mengubah data atau status pinjam |
| Delete | DELETE | /equipment/{id} | Menghapus alat |

## 5. Arsitektur dan alur data
Client -> Function URL -> Lambda -> S3, dengan log di CloudWatch.
1. Client mengirim request HTTPS ke Function URL.
2. Function URL meneruskan request ke fungsi Lambda.
3. Lambda membaca, menulis, atau menghapus objek JSON di bucket S3.
4. Hasil dikembalikan sebagai JSON ke client.
Diagram: docs/architecture.png

## 6. IAM dan keamanan
- Lambda memakai execution role LabRole (bawaan Learner Lab) dengan
  izin ke S3 dan CloudWatch Logs.
- Bucket S3 bersifat privat (Block Public Access aktif); hanya Lambda
  yang mengaksesnya.
- Function URL memakai auth type NONE agar mudah diuji dengan curl.
  Konsekuensinya endpoint dapat dipanggil siapa pun yang mengetahui URL-nya,
  sehingga URL tidak dipublikasikan di repository.
- Tidak ada kredensial di dalam repository.
- Tidak memakai VPC karena seluruh layanan adalah managed service.

## 7. Rencana deployment
Lihat deployment/deployment-plan.md

## 8. Rencana pengujian dan bukti
Uji tiap endpoint dengan curl atau Postman, lalu lampirkan screenshot
bucket S3, konfigurasi Lambda, Function URL, output uji, dan log
CloudWatch di docs/evidence/.
