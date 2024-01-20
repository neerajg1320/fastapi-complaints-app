import base64
from fastapi import HTTPException


def decode_photo(path, encoded_str):
    with open(path, "wb") as f:
        try:
            # The following needs to be verified. The encode operation seems redundant
            f.write(base64.b64decode(encoded_str.encode("utf-8")))
        except Exception as ex:
            raise HTTPException(400, "Invalid photo encoding")

