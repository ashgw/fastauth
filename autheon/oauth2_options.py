from __future__ import annotations

from logging import Logger

from fastapi import APIRouter

from autheon.providers.base import Provider
from autheon.libtypes import FallbackSecrets
from autheon.signin import SignInCallback
from autheon.const_data import CookieData
from autheon.adapters.fastapi.flow import FastAPIOAuthFlow as FastAPIOAuth2
from autheon.log import logger as flogger
from autheon.config import AuthConfig


def OAuthOptions(
    provider: Provider,
    fallback_secrets: FallbackSecrets,
    signin_callback: SignInCallback,
    signin_uri: str = "/auth/signin",
    signout_url: str = "/auth/signout",
    callback_uri: str = "/auth/callback",
    jwt_uri: str = "/auth/jwt",
    csrf_token_uri: str = "/auth/csrf-token",
    post_signin_uri: str = "/auth/in",
    post_signout_uri: str = "/auth/out",
    error_uri: str = "/auth/error",
    jwt_max_age: int = CookieData.JWT.max_age,
    debug: bool = True,
    logger: Logger = flogger,
) -> APIRouter:
    AuthConfig.set_defaults(debug=debug, logger=logger)
    auth = FastAPIOAuth2(
        provider=provider,
        fallback_secrets=fallback_secrets,
        signin_callback=signin_callback,
        signin_uri=signin_uri,
        signout_url=signout_url,
        callback_uri=callback_uri,
        jwt_uri=jwt_uri,
        csrf_token_uri=csrf_token_uri,
        post_signin_uri=post_signin_uri,
        post_signout_uri=post_signout_uri,
        error_uri=error_uri,
        jwt_max_age=jwt_max_age,
    )
    return auth.auth_route
