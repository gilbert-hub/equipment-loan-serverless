# Equipment Loan API

Aplikasi peminjaman alat berbasis serverless di AWS.
Track C (Serverless) - Tugas Individu Komputasi Awan, Week 12.

## Use case
Peminjaman alat: mencatat alat, status ketersediaan, dan peminjamnya.

## Arsitektur
Client → Lambda Function URL → Lambda → S3 (+ CloudWatch Logs)

![Arsitektur](docs/architecture.png)

Detail desain: [docs/design-brief.md](docs/design-brief.md)

## Entitas
Equipment: id, name, category, status, borrower, borrowed_at, due_date

Setiap alat disimpan sebagai satu objek JSON di S3 dengan key `equipment/{id}.json`.

## Endpoint CRUD
| Method | Path | Fungsi |
|---|---|---|
| POST | /equipment | Tambah alat |
| GET | /equipment | Daftar alat |
| GET | /equipment/{id} | Detail alat |
| PUT | /equipment/{id} | Ubah data/status |
| DELETE | /equipment/{id} | Hapus alat |

## Struktur repository
```
├── README.md
├── docs/            diagram arsitektur, design brief, bukti AWS
├── lambda/          kode fungsi Lambda
└── deployment/      rencana deployment
```

## Rencana deployment
Lihat [deployment/deployment-plan.md](deployment/deployment-plan.md)

## Cara mereproduksi
1. Buat bucket S3 (region us-east-1) dengan Block Public Access tetap aktif.
2. Buat fungsi Lambda dari `lambda/lambda_function.py` dengan role LabRole,
   lalu set environment variable `BUCKET_NAME=<nama-bucket>`.
3. Aktifkan Function URL pada fungsi Lambda tersebut.
4. Uji dengan curl (contoh di bawah).

## Contoh pengujian
Ganti `<FUNCTION_URL>` dengan URL Function URL (tanpa garis miring di akhir).

```bash
# Create
curl -X POST <FUNCTION_URL>/equipment -H "Content-Type: application/json" \
  -d '{"id":"eq-001","name":"Proyektor Epson","category":"Elektronik","status":"available"}'

# Read (daftar dan detail)
curl <FUNCTION_URL>/equipment
curl <FUNCTION_URL>/equipment/eq-001

# Update
curl -X PUT <FUNCTION_URL>/equipment/eq-001 -H "Content-Type: application/json" \
  -d '{"status":"borrowed","borrower":"Gilbert","due_date":"2026-12-01"}'

# Delete
curl -X DELETE <FUNCTION_URL>/equipment/eq-001
```

## Status
- [x] Repo dibuat
- [x] Design brief
- [x] Rencana deployment
- [x] Diagram arsitektur diunggah
- [ ] Bucket S3
- [ ] Lambda
- [ ] Function URL
- [ ] Bukti uji koneksi (docs/evidence/)

## Catatan keamanan
Tidak ada kredensial AWS di repository ini.
