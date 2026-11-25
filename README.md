# Equipment Loan API

Aplikasi peminjaman alat berbasis serverless di AWS.
Track C - Tugas Individu Komputasi Awan, Week 12.

## Use case
Peminjaman alat: mencatat alat, status ketersediaan, dan peminjamnya.

## Arsitektur
Client → API Gateway → Lambda → DynamoDB (+ CloudWatch Logs)
Diagram: docs/architecture.png

## Entitas
Equipment: id, name, category, status, borrower, borrowed_at, due_date

## Endpoint CRUD
| Method | Path | Fungsi |
|---|---|---|
| POST | /equipment | Tambah alat |
| GET | /equipment | Daftar alat |
| GET | /equipment/{id} | Detail alat |
| PUT | /equipment/{id} | Ubah data/status |
| DELETE | /equipment/{id} | Hapus alat |

## Rencana deployment
Lihat deployment/deployment-plan.md

## Cara mereproduksi
1. Buat tabel DynamoDB `Equipment` (partition key `id`, String, on-demand), region us-east-1.
2. Buat fungsi Lambda dari `lambda/lambda_function.py` dengan role LabRole.
3. Buat API Gateway dan sambungkan route ke Lambda.
4. Uji dengan curl (contoh di bawah).

## Status
- [x] Repo dibuat
- [ ] Tabel DynamoDB
- [ ] Lambda
- [ ] API Gateway
- [ ] Bukti uji koneksi
