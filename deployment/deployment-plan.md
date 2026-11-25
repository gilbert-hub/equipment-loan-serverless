# Deployment Plan - Equipment Loan API (Track C: Serverless)

## Lingkungan
- Platform: AWS Learner Lab
- Region: us-east-1
- Peran IAM: LabRole (bawaan Learner Lab)

## Urutan deployment
1. **S3**
   - Bucket: `<nama-bucket-unik>` (nama bucket harus unik secara global)
   - Block Public Access: aktif (bucket privat)
   - Objek data disimpan dengan prefix `equipment/`
2. **Lambda**
   - Nama fungsi: `equipment-handler`
   - Runtime: Python 3.x
   - Execution role: LabRole
   - Timeout: 10 detik (bawaan 3 detik terlalu singkat)
   - Environment variable: `BUCKET_NAME=<nama-bucket-unik>`
3. **Function URL**
   - Dibuat dari tab Configuration pada fungsi Lambda
   - Auth type: NONE (untuk pengujian)
   - Satu URL untuk semua route; kode Lambda memilah method dan path
4. **Pengujian**
   - Uji tiap endpoint dengan curl/Postman
   - Cek log di CloudWatch Logs

## Pengelolaan biaya
- Lambda dan S3 hanya menagih sesuai pemakaian.
- Tidak memakai EC2, RDS, NAT Gateway, atau Load Balancer.
- Resource dihapus jika tidak diperlukan lagi.

## Verifikasi
- Screenshot: bucket S3 beserta objeknya, konfigurasi Lambda,
  Function URL, output curl, dan log CloudWatch
  (disimpan di docs/evidence/).
