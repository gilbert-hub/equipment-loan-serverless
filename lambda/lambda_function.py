import base64
import json
import os
import re

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
PREFIX = "equipment/"
s3 = boto3.client("s3")

ALLOWED_FIELDS = ["name", "category", "status", "borrower", "borrowed_at", "due_date"]
VALID_STATUS = ["available", "borrowed"]
ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def key_for(item_id):
    return f"{PREFIX}{item_id}.json"


def parse_body(event):
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def read_item(item_id):
    """Baca satu objek dari S3. Kembalikan None jika tidak ada."""
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key_for(item_id))
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchKey", "404"):
            return None
        raise
    return json.loads(obj["Body"].read())


def write_item(item):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key_for(item["id"]),
        Body=json.dumps(item).encode("utf-8"),
        ContentType="application/json",
    )


def create_item(event):
    data = parse_body(event)
    if data is None:
        return response(400, {"message": "Body bukan JSON object yang valid"})
    item_id = str(data.get("id", ""))
    if not ID_PATTERN.match(item_id) or not data.get("name"):
        return response(
            400,
            {"message": "id (huruf, angka, - atau _, maks 64) dan name wajib diisi"},
        )
    if data.get("status", "available") not in VALID_STATUS:
        return response(400, {"message": "status harus available atau borrowed"})
    if read_item(item_id) is not None:
        return response(409, {"message": "id sudah ada"})

    item = {"id": item_id, "status": data.get("status", "available")}
    for field in ALLOWED_FIELDS:
        if field in data and field != "status":
            item[field] = data[field]
    write_item(item)
    return response(201, item)


def list_items():
    items = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=PREFIX):
        for obj in page.get("Contents", []):
            if not obj["Key"].endswith(".json"):
                continue
            body = s3.get_object(Bucket=BUCKET_NAME, Key=obj["Key"])["Body"].read()
            items.append(json.loads(body))
    return response(200, items)


def get_item(item_id):
    item = read_item(item_id)
    if item is None:
        return response(404, {"message": "Alat tidak ditemukan"})
    return response(200, item)


def update_item(item_id, event):
    data = parse_body(event)
    if data is None:
        return response(400, {"message": "Body bukan JSON object yang valid"})
    if "status" in data and data["status"] not in VALID_STATUS:
        return response(400, {"message": "status harus available atau borrowed"})

    fields = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}
    if not fields:
        return response(400, {"message": "Tidak ada field yang bisa diubah"})

    item = read_item(item_id)
    if item is None:
        return response(404, {"message": "Alat tidak ditemukan"})
    item.update(fields)
    write_item(item)
    return response(200, item)


def delete_item(item_id):
    if read_item(item_id) is None:
        return response(404, {"message": "Alat tidak ditemukan"})
    s3.delete_object(Bucket=BUCKET_NAME, Key=key_for(item_id))
    return response(200, {"message": "Alat dihapus", "id": item_id})


def lambda_handler(event, context):
    http = event.get("requestContext", {}).get("http", {})
    method = http.get("method", "")
    path = event.get("rawPath", "").rstrip("/")
    print(f"Request: {method} {path}")

    if not BUCKET_NAME:
        return response(500, {"message": "BUCKET_NAME belum diatur"})

    parts = [p for p in path.split("/") if p]
    try:
        if parts == ["equipment"]:
            if method == "POST":
                return create_item(event)
            if method == "GET":
                return list_items()
        elif len(parts) == 2 and parts[0] == "equipment":
            item_id = parts[1]
            if not ID_PATTERN.match(item_id):
                return response(400, {"message": "Format id tidak valid"})
            if method == "GET":
                return get_item(item_id)
            if method == "PUT":
                return update_item(item_id, event)
            if method == "DELETE":
                return delete_item(item_id)
        return response(404, {"message": f"Route tidak dikenal: {method} {path}"})
    except Exception as e:
        print(f"Error: {e}")
        return response(500, {"message": "Terjadi kesalahan pada server"})
