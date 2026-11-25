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
1. Buat bucket S3 (region `us-east-1`) dengan Block Public Access tetap aktif.
2. Buat fungsi Lambda dari `lambda/lambda_function.py` dengan role `LabRole`,
   lalu set environment variable `BUCKET_NAME=<nama-bucket>`.
3. Aktifkan Function URL pada fungsi Lambda tersebut (Auth type: `NONE`).
4. Uji dengan `curl` (contoh di bawah).

## Contoh pengujian
Endpoint aktif yang digunakan pada saat pengujian:
`https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws` *(catatan: URL bersifat sementara mengikuti sesi AWS Learner Lab; perlu pergantian terhadap `<FUNCTION_URL>` jika melakukan deployment ulang)*.

```bash
# Create
curl -i -X POST "[https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment](https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment)" \
  -H "Content-Type: application/json" \
  -d '{"id":"eq-001","name":"Proyektor Epson EB-X500","category":"elektronik"}'

# Read (daftar dan detail)
curl -i "[https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment](https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment)"
curl -i "[https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment/eq-001](https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment/eq-001)"

# Update
curl -i -X PUT "[https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment/eq-001](https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment/eq-001)" \
  -H "Content-Type: application/json" \
  -d '{"status":"borrowed","borrower":"Gilbert Nainggolan","borrowed_at":"2026-11-26","due_date":"2026-11-30"}'

# Delete
curl -i -X DELETE "[https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment/eq-001](https://so73vqs5eeozpb3ocbz5hgxpue0mmsum.lambda-url.us-east-1.on.aws/equipment/eq-001)"
```

Hasil pengujian lengkap dapat dilihat di [docs/evidence/README.md](docs/evidence/README.md).

## Status
- [x] Repo dibuat
- [x] Design brief
- [x] Rencana deployment
- [x] Diagram arsitektur diunggah
- [x] Bucket S3 (`equipment-loan-gshn`)
- [x] Lambda (`equipment-handler`)
- [x] Function URL
- [x] Bukti uji koneksi ([docs/evidence/](docs/evidence/README.md))

## Catatan keamanan
Tidak ada kredensial AWS (Access Key maupun Secret Key) di repository ini.
