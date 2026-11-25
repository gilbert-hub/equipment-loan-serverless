# Equipment Loan API

Aplikasi peminjaman alat berbasis serverless di AWS.
Track C (Serverless) - Tugas Individu Komputasi Awan, Week 12.

## Use case
Peminjaman alat: mencatat alat, status ketersediaan, dan peminjamnya.

## Arsitektur
Client → API Gateway → Lambda → DynamoDB (+ CloudWatch Logs)

![Arsitektur](docs/architecture.png)

Detail desain: [docs/design-brief.md](docs/design-brief.md)

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
1. Buat tabel DynamoDB `Equipment` (partition key `id`, String, on-demand), region us-east-1.
2. Buat fungsi Lambda dari `lambda/lambda_function.py` dengan role LabRole,
   lalu set environment variable `TABLE_NAME=Equipment`.
3. Buat API Gateway (HTTP API) dan sambungkan kelima route ke fungsi Lambda.
4. Uji dengan curl (contoh di bawah).

## Contoh pengujian
Ganti `<API_URL>` dengan URL invoke API Gateway.

```bash
# Create
curl -X POST <API_URL>/equipment -H "Content-Type: application/json" \
  -d '{"id":"eq-001","name":"Proyektor Epson","category":"Elektronik","status":"available"}'

# Read (daftar dan detail)
curl <API_URL>/equipment
curl <API_URL>/equipment/eq-001

# Update
curl -X PUT <API_URL>/equipment/eq-001 -H "Content-Type: application/json" \
  -d '{"status":"borrowed","borrower":"Gilbert","due_date":"2026-12-01"}'

# Delete
curl -X DELETE <API_URL>/equipment/eq-001
```

## Status
- [x] Repo dibuat
- [x] Design brief
- [x] Rencana deployment
- [x] Diagram arsitektur diunggah
- [ ] Tabel DynamoDB
- [ ] Lambda
- [ ] API Gateway
- [ ] Bukti uji koneksi (docs/evidence/)

## Catatan keamanan
Tidak ada kredensial AWS di repository ini.
