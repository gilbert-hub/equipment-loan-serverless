import json
import os
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("TABLE_NAME", "Equipment")
table = boto3.resource("dynamodb").Table(TABLE_NAME)

ALLOWED_FIELDS = ["name", "category", "status", "borrower", "borrowed_at", "due_date"]
VALID_STATUS = ["available", "borrowed"]


def _default(o):
    if isinstance(o, Decimal):
        return int(o) if o % 1 == 0 else float(o)
    raise TypeError


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=_default),
    }


def parse_body(event):
    try:
        return json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return None


def create_item(event):
    data = parse_body(event)
    if data is None:
        return response(400, {"message": "Body bukan JSON yang valid"})
    if not data.get("id") or not data.get("name"):
        return response(400, {"message": "Field id dan name wajib diisi"})
    if data.get("status", "available") not in VALID_STATUS:
        return response(400, {"message": "status harus available atau borrowed"})

    item = {"id": str(data["id"]), "status": data.get("status", "available")}
    for field in ALLOWED_FIELDS:
        if field in data and field != "status":
            item[field] = data[field]

    try:
        table.put_item(Item=item, ConditionExpression="attribute_not_exists(id)")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return response(409, {"message": "id sudah ada"})
        raise
    return response(201, item)


def list_items():
    result = table.scan()
    items = result.get("Items", [])
    while "LastEvaluatedKey" in result:
        result = table.scan(ExclusiveStartKey=result["LastEvaluatedKey"])
        items.extend(result.get("Items", []))
    return response(200, items)


def get_item(item_id):
    result = table.get_item(Key={"id": item_id})
    item = result.get("Item")
    if not item:
        return response(404, {"message": "Alat tidak ditemukan"})
    return response(200, item)


def update_item(item_id, event):
    data = parse_body(event)
    if data is None:
        return response(400, {"message": "Body bukan JSON yang valid"})
    if "status" in data and data["status"] not in VALID_STATUS:
        return response(400, {"message": "status harus available atau borrowed"})

    fields = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}
    if not fields:
        return response(400, {"message": "Tidak ada field yang bisa diubah"})

    names = {f"#{k}": k for k in fields}
    values = {f":{k}": v for k, v in fields.items()}
    expression = "SET " + ", ".join(f"#{k} = :{k}" for k in fields)

    try:
        result = table.update_item(
            Key={"id": item_id},
            UpdateExpression=expression,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
            ConditionExpression="attribute_exists(id)",
            ReturnValues="ALL_NEW",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return response(404, {"message": "Alat tidak ditemukan"})
        raise
    return response(200, result["Attributes"])


def delete_item(item_id):
    try:
        table.delete_item(
            Key={"id": item_id}, ConditionExpression="attribute_exists(id)"
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return response(404, {"message": "Alat tidak ditemukan"})
        raise
    return response(200, {"message": "Alat dihapus", "id": item_id})


def lambda_handler(event, context):
    route = event.get("routeKey", "")
    item_id = (event.get("pathParameters") or {}).get("id")
    print(f"Route: {route}")

    try:
        if route == "POST /equipment":
            return create_item(event)
        if route == "GET /equipment":
            return list_items()
        if route == "GET /equipment/{id}":
            return get_item(item_id)
        if route == "PUT /equipment/{id}":
            return update_item(item_id, event)
        if route == "DELETE /equipment/{id}":
            return delete_item(item_id)
        return response(404, {"message": f"Route tidak dikenal: {route}"})
    except Exception as e:
        print(f"Error: {e}")
        return response(500, {"message": "Terjadi kesalahan pada server"})
