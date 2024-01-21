import requests
import json
import uuid
from fastapi  import HTTPException
from decouple import config


class WiseService:
    def __init__(self):
        self.base_url = config("WISE_SANDBOX_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = f"{self.base_url}/v2/profiles"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response = response.json()
            ids = [el["id"] for el in response if el["type"] == "BUSINESS"]
            if len(ids) > 0:
                return ids[0]
            raise HTTPException(500, "Invalid response from payment provider")
        print(response)
        raise HTTPException(500, "Payment provider is not available")

    def create_quote(self, amount):
        url = f"{self.base_url}/v3/quotes"
        data = {
            "sourceCurrency": "GBP",
            "targetCurrency": "USD",
            "sourceAmount": amount,
            "profile": self.profile_id
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            response = response.json()
            print(json.dumps(response, indent=2))
            return response["id"]
        print("Error!", response.json())
        raise HTTPException(500, "Payment provider is not available")

    def create_recipient_account(self, full_name, iban):
        url =f"{self.base_url}/v1/accounts"
        data = {
          "currency": "GBP",
          "type": "sort_code",
          "profile": self.profile_id,
          "ownedByCustomer": True,
          "accountHolderName": "John Doe",
           "details": {
              "legalType": "PRIVATE",
              "sortCode": "040075",
              "accountNumber": "37778842"
           }
         }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            response = response.json()
            return response["id"]
        print("Error!", response.json())
        raise HTTPException(500, "Payment provider is not available")

    def create_transfer(self, target_account_id, quote_id):
       customer_transfer_id = str(uuid.uuid4())
       url =f"{self.base_url}/v1/transfers"
       data = {
          "sourceAccount": target_account_id,
          "targetAccount": target_account_id,
          "quoteUuid": quote_id,
          "customerTransactionId": customer_transfer_id,
          "details" : {
              "reference" : "to my friend",
              "transferPurpose": "verification.transfers.purpose.pay.bills",
              "transferPurposeSubTransferPurpose": "verification.sub.transfers.purpose.pay.interpretation.service",
              "sourceOfFunds": "verification.source.of.funds.other"
            }
         }
       response = requests.post(url, headers=self.headers, data=json.dumps(data))
       if response.status_code == 200:
           response = response.json()
           return response["id"]
       print("Error!", response.json())
       raise HTTPException(500, "Payment provider is not available")

if __name__ == "__main__":
    w = WiseService()
    print("Profile ID: ", w.profile_id)
    quote_id = w.create_quote(50)
    print("Quote ID: ", quote_id)
    recipient_id = w.create_recipient_account("Alice Kohn", "BR1500000000000010932840814P2")
    print("Recipient ID: ", recipient_id)
    # print(type(response), json.dumps(response, indent=2))
    transter = w.create_transfer(recipient_id, quote_id)
