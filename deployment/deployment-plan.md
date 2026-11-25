# Deployment Plan - Equipment Loan API (Track C: Serverless)

## Lingkungan
- Platform: AWS Learner Lab
- Region: us-east-1
- Peran IAM: LabRole (bawaan Learner Lab)

## Urutan deployment
1. **DynamoDB**
   - Tabel: `Equipment`
   - Partition key: `id` (String)
   - Mode kapasitas: On-demand
2. **Lambda**
   - Nama fungsi: `equipment-handler`
   - Runtime: Python 3.x
   - Execution role: LabRole
   - Environment variable: `TABLE_NAME=Equipment`
3. **API Gateway (HTTP API)**
   - Route: POST /equipment, GET /equipment, GET /equipment/{id},
     PUT /equipment/{id}, DELETE /equipment/{id}
   - Integrasi: Lambda proxy ke `equipment-handler`
4. **Pengujian**
   - Uji tiap endpoint dengan curl/Postman
   - Cek log di CloudWatch Logs

## Pengelolaan biaya
- DynamoDB on-demand dan Lambda hanya menagih sesuai pemakaian.
- Tidak memakai EC2, RDS, NAT Gateway, atau Load Balancer.
- Resource dihapus jika tidak diperlukan lagi.

## Verifikasi
- Screenshot: tabel DynamoDB, konfigurasi Lambda, route API Gateway,
  output curl, dan log CloudWatch (disimpan di docs/evidence/).
