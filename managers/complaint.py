import uuid
import os
from constants import TEMP_FILES_FOLDER
from models import complaint, transaction
from models import RoleType, ComplaintState
from db import database
from services.s3 import S3Service
from services.ses import SESService
from services.wise import WiseService
from utils.helpers import decode_photo


s3 = S3Service()
ses = SESService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.state == ComplaintState.pending)

        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo")
        extension =  complaint_data.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILES_FOLDER, name)

        # decode the string in encoded photo and store in path
        decode_photo(path, encoded_photo)
        # upload to AWS S3 bukcet and save the url
        complaint_data['photo_url'] = s3.upload(path, name, extension)

        id_ = await database.execute(complaint.insert().values(complaint_data))
        # We are inserting transaction here ??
        await ComplaintManager.issue_transaction(
            complaint_data["amount"],
            f"{user['first_name']} {user['last_name']}",
            user["iban"],
            id_
        )
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete_complaint(complaint_id):
        return await database.execute(
            complaint.delete().where(complaint.c.id == complaint_id)
        )

    @staticmethod
    async def approve(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=ComplaintState.approved)
        )

        # TBD: Check if we can prevent this database read
        transaction_data = database.fetch_one(transaction.select().where(transaction.c.complaint_id == id_))

        # TBD: Need to abstract
        wise = WiseService()

        # Need to solve by fixing the quote bug
        # wise.fund_transfer(transaction_data["transfer_id"])

        # Later we will replace it with the user's email
        ses.send_mail("Complaint Approved",
                      ["neeraj76@yahoo.com"],
                      "Congrats! your claim is approved"
                      )

    @staticmethod
    async def reject(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=ComplaintState.rejected)
        )
        # Later we will replace it with the user's email
        ses.send_mail("Complaint Rejected",
                      ["neeraj76@yahoo.com"],
                      "Your claim has been rejected"
                      )

    @staticmethod
    async def issue_transaction(amount, full_name, iban, complaint_id):
        wise = WiseService()
        quote_id = wise.create_quote(amount)
        recipient_id = wise.create_recipient_account(full_name, iban)
        # We have commented this as we are facing some problem in sandbox
        # transfer_id = wise.create_transfer(recipient_id, quote_id)
        transfer_id = 0x45

        data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": str(recipient_id),
            "amount": amount,
            "complaint_id": complaint_id,
        }

        await database.execute(transaction.insert().values(**data))