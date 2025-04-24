from config import boto3_conf

def upload_s3(file, filename):

    boto3_conf.s3_client.upload_fileobj(
                    Fileobj=file,
                    Bucket=boto3_conf.S3_BUCKET_NAME,
                    Key=filename,
                    ExtraArgs={"ACL": "public-read"}
                )
    file_url = f"https://s3.cloud.ru/{boto3_conf.S3_BUCKET_NAME}/{filename}"

    return file_url
