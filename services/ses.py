import boto3
from decouple import config
from fastapi import HTTPException
from services.base import AWSService


class SESService(AWSService):
    def __init__(self):
        super().__init__()
        self.ses_region = config("AWS_BUCKET_REGION")
        self.ses = boto3.client("ses",
                               region_name=self.ses_region,
                               aws_access_key_id=self.key,
                               aws_secret_access_key=self.secret
                               )

    def send_mail(self, subject, to_addresses, text_data):
        subject = {"Data": subject, "Charset": "UTF-8"}
        body = {"Text": {"Data": text_data, "Charset": "UTF-8"}}
        self.ses.send_email(Source="neerajgupta.mbox@gmail.com",
                            Destination={"ToAddresses": to_addresses,
                                         "CcAddresses": [],
                                         "BccAddresses": []
                                         },
                            Message={"Subject": subject, "Body": body},
                            )