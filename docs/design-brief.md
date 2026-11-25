# Design Brief - Equipment Loan API

Tugas Individu Komputasi Awan, Week 12 - Design & AWS Setup
Nama: Gilbert S. H. Nainggolan

## 1. Use case
Sistem peminjaman alat untuk mencatat alat yang tersedia, siapa yang
meminjam, dan kapan alat harus dikembalikan. Pengguna dapat menambah alat,
melihat daftar dan detail alat, memperbarui status peminjaman, serta
menghapus alat yang tidak dipakai lagi.

## 2. Track yang dipilih
Track C - Serverless: API Gateway + AWS Lambda + Amazon DynamoDB.

Alasan pemilihan:
- Data hanya satu entitas tanpa relasi kompleks, sehingga cocok untuk
  DynamoDB.
- Tidak perlu mengelola server maupun jaringan (VPC).
- Biaya mengikuti pemakaian, sehingga hemat untuk budget Learner Lab
  yang tidak dapat di-reset.

## 3. Entitas data
Equipment

| Atribut | Tipe | Keterangan |
|---|---|---|
| id | String (partition key) | Pengenal unik, contoh: eq-001 |
| name | String | Nama alat |
| category | String | Kategori alat |
| status | String | available / borrowed |
| borrower | String | Nama peminjam (kosong jika tersedia) |
| borrowed_at | String | Tanggal pinjam |
| due_date | String | Batas tanggal kembali |

## 4. Endpoint CRUD
| Operasi | Method | Path | Fungsi |
|---|---|---|---|
| Create | POST | /equipment | Menambah alat baru |
| Read | GET | /equipment, /equipment/{id} | Daftar atau detail alat |
| Update | PUT | /equipment/{id} | Mengubah data atau status pinjam |
| Delete | DELETE | /equipment/{id} | Menghapus alat |

## 5. Arsitektur dan alur data
Client -> API Gateway -> Lambda -> DynamoDB, dengan log di CloudWatch.
1. Client mengirim request HTTPS ke API Gateway.
2. API Gateway meneruskan request ke fungsi Lambda (proxy integration).
3. Lambda menjalankan operasi CRUD pada tabel DynamoDB `Equipment`.
4. Hasil dikembalikan sebagai JSON melalui API Gateway.
Diagram: docs/architecture.png

## 6. IAM dan keamanan
- Lambda memakai execution role LabRole (bawaan Learner Lab) dengan
  izin ke DynamoDB.
- Komunikasi client melalui HTTPS.
- Tidak ada kredensial di dalam repository.
- Tidak memakai VPC karena seluruh layanan adalah managed service.

## 7. Rencana deployment
Lihat deployment/deployment-plan.md

## 8. Rencana pengujian dan bukti
Uji tiap endpoint dengan curl atau Postman, lalu lampirkan screenshot
tabel DynamoDB, konfigurasi Lambda, route API Gateway, output uji,
dan log CloudWatch di docs/evidence/.
