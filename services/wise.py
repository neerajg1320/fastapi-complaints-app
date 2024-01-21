import requests
from fastapi  import HTTPException
from decouple import config


class WiseService:
    def __init__(self):
        self.main_url = ""
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = "https://api.sandbox.transferwise.tech/v2/profiles"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response = response.json()
            # return [el["id"] for el in response]
            return [el["id"] for el in response if el["type"] == "PERSONAL"]
        print(response)
        raise HTTPException(500, "Payment provider is not available")

if __name__ == "__main__":
    w = WiseService()
    print(w.profile_id)

