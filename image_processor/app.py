import io
import os
import boto3
from PIL import Image

s3 = boto3.client("s3")

INPUT_PREFIX = "raw-uploads/"
OUTPUT_PREFIX = "optimized-delivery/"
MAX_WIDTH = 400
WEBP_QUALITY = 80


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        if not key.startswith(INPUT_PREFIX) or key.endswith("/"):
            print(f"Skipping {key} — not a processable image")
            continue

        print(f"Processing s3://{bucket}/{key}")

        response = s3.get_object(Bucket=bucket, Key=key)
        image_bytes = response["Body"].read()

        with Image.open(io.BytesIO(image_bytes)) as img:
            img = _to_rgb(img)
            img = _resize(img, MAX_WIDTH)

            buffer = io.BytesIO()
            img.save(buffer, format="WEBP", quality=WEBP_QUALITY)
            buffer.seek(0)

        output_key = _build_output_key(key)
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=buffer,
            ContentType="image/webp",
        )
        print(f"Saved optimized image to s3://{bucket}/{output_key}")

    return {"statusCode": 200, "body": "OK"}


def _to_rgb(img: Image.Image) -> Image.Image:
    # WEBP encoder requires RGB or RGBA; convert palette/CMYK modes
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    return img


def _resize(img: Image.Image, max_width: int) -> Image.Image:
    if img.width <= max_width:
        return img
    ratio = max_width / img.width
    new_size = (max_width, int(img.height * ratio))
    return img.resize(new_size, Image.LANCZOS)


def _build_output_key(key: str) -> str:
    # raw-uploads/photos/foo.jpeg  ->  optimized-delivery/photos/foo.webp
    relative = key[len(INPUT_PREFIX):]
    stem = os.path.splitext(relative)[0]
    return f"{OUTPUT_PREFIX}{stem}.webp"
