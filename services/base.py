from decouple import config


class AWSService:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET_KEY")
        self.bucket = config("AWS_BUCKET_NAME")
        self.region = config("AWS_BUCKET_REGION")
