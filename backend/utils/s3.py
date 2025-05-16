from config import boto3_conf, app_conf
from io import BytesIO  
from models import db
from models.media import Media

def upload_s3(file: str, filename: str) -> str:

    boto3_conf.s3_client.upload_fileobj(
                    Fileobj=file,
                    Bucket=boto3_conf.S3_BUCKET_NAME,
                    Key=filename,
                    ExtraArgs={"ACL": "public-read"}
                )
    file_url = f"https://s3.cloud.ru/{boto3_conf.S3_BUCKET_NAME}/{filename}"

    return file_url



def get_file_s3(s3_key: str) -> bytes:
    with app_conf.app.app_context():
        media = db.session.query(Media).filter_by(s3_key=s3_key).first()
        if not media:
            raise ValueError(f"Media with s3_key {s3_key} not found")
        file = boto3_conf.s3_client.get_object(Bucket=boto3_conf.S3_BUCKET_NAME, Key=media.s3_key)
        return file['Body'].read()
