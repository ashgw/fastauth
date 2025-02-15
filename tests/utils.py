from typing import Optional

from starlette.responses import RedirectResponse

from autheon.libtypes import UserInfo, AccessToken
from autheon.providers.base import Provider


def get_method_to_patch(*, patched_class: object, method_name: str) -> str:
    if not hasattr(patched_class, method_name):
        raise AttributeError(
            f"The method '{method_name}' does not exist on the class '{patched_class.__qualname__}'"
        )
    method_to_patch = (
        f"{patched_class.__module__}.{patched_class.__qualname__}.{method_name}"
    )
    return method_to_patch


class MockProvider(Provider):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            provider="mock",
            authorizationUrl="https://accounts.exmaple.com/authorize",
            tokenUrl="https://accounts.exmaple.com/api/token",
            userInfo="https://api.exmaple.com/v1/me",
        )

    def authorize(
        self, *, state: str, code_challenge: str, code_challenge_method: str
    ) -> RedirectResponse:  # pragma: no cover
        return RedirectResponse("/")

    async def get_access_token(
        self, *, code_verifier: str, code: str, state: str
    ) -> Optional[AccessToken]:  # pragma: no cover
        _ = await self._request_access_token(
            code_verifier=code_verifier, code=code, state=state
        )
        return AccessToken("...")

    async def get_user_info(
        self, _access_token: str
    ) -> Optional[UserInfo]:  # pragma: no cover
        _ = await self._request_user_info(access_token=_access_token)
        return UserInfo(user_id="...", name="...", avatar="...", email="...")
