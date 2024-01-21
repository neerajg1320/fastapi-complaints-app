import requests
import json
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
            ids = [el["id"] for el in response if el["type"] == "PERSONAL"]
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
            return response["id"]
        print("Error!", response)
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
            return response
        print("Error!", response.json())
        # raise HTTPException(500, "Payment provider is not available")

if __name__ == "__main__":
    w = WiseService()
    print(w.profile_id)
    # response = w.create_quote(50)
    response = w.create_recipient_account("Alice Kohn", "BR1500000000000010932840814P2")
    print(type(response), json.dumps(response, indent=2))

