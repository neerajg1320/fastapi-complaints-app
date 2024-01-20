import boto3
from fastapi import HTTPException
from services.base import AWSService


class S3Service(AWSService):
    def __init__(self):
        super().__init__()
        self.s3 = boto3.client("s3",
                               aws_access_key_id=self.key,
                               aws_secret_access_key=self.secret
                               )

    def upload(self, path, key, ext):
        try:
            self.s3.upload_file(path, self.bucket, key,
                                ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"}
                                )
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        except Exception as ex:
            raise HTTPException(500, "S3 is not available")
