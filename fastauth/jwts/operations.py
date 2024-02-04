from jose.jwt import encode as encode_jwt
from jose.jwt import decode as decode_jwt
from jose.exceptions import JOSEError
from jose.jwt import ALGORITHMS
from jose.jwe import encrypt, decrypt
from datetime import datetime, timedelta
from fastauth.data import CookiesData
from fastauth.jwts.helpers import validate_secret_key
from fastauth._types import JWT, UserInfo, FallbackSecrets
from typing import Optional

JWT_MAX_AGE = CookiesData.JWT.max_age
JWT_ALGORITHM = ALGORITHMS.HS256
JWE_ALGORITHM = ALGORITHMS.A256GCM
ISSUER = "fastauth"
SUBJECT = "client"


def encipher_user_info(
    user_info: UserInfo,
    fallback_secrets: FallbackSecrets,
    max_age: int = JWT_MAX_AGE,
) -> str:
    now = datetime.utcnow()
    e: Optional[JOSEError] = None
    for secret in fallback_secrets:
        key = validate_secret_key(secret)
        try:
            plain_jwt: str = encode_jwt(
                claims=JWT(
                    iss=ISSUER,
                    sub=SUBJECT,
                    iat=now,
                    exp=now + timedelta(seconds=max_age),
                    user_info=user_info,
                ),
                key=key,
                algorithm=JWT_ALGORITHM,
            )

            encrypted_jwt: str = (
                encrypt(
                    plaintext=plain_jwt.encode(),
                    key=key,
                    algorithm=ALGORITHMS.DIR,
                    encryption=JWE_ALGORITHM,
                )
                .rstrip(b"=")
                .decode()
            )

            return encrypted_jwt
        except JOSEError as exc:
            e = exc
    if e is not None:
        raise e
    else:
        raise JOSEError("Failed to encipher user info with all the provided keys")


def decipher_jwt(encrypted_jwt: str, fallback_secrets: FallbackSecrets) -> JWT:
    e: Optional[JOSEError] = None
    for secret in fallback_secrets:
        key = validate_secret_key(secret)
        try:
            decrypted_jwt: str = (
                decrypt(jwe_str=encrypted_jwt, key=key).rstrip(b"=").decode()
            )
            jwt: JWT = decode_jwt(
                token=decrypted_jwt,
                key=key,
                algorithms=JWT_ALGORITHM,
                issuer=ISSUER,
                subject=SUBJECT,
            )
            return jwt
        except JOSEError as exc:
            e = exc
    if e is not None:
        raise e
    else:
        raise JOSEError("Failed to decipher user info with all the provided keys")
