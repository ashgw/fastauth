from .utils import MockProvider
from fastauth.grant_redirect import AuthGrantRedirect


def test_oauth_redirect_url() -> None:
    pv = MockProvider(
        client_id="client_id",
        client_secret="client_secret",
        redirect_uri="https://mysite.com/auth/callback/mock",
    )
    redirect = AuthGrantRedirect(
        provider=pv,
        state="state",
        code_challenge="code_challenge",
        code_challenge_method="s256",
    )
    assert (
        redirect.url
        == "https://accounts.exmaple.com/authorize?response_type=code&client_id=client_id&redirect_uri=https://mysite.com/auth/callback/mock&state=state&code_challenge=code_challenge&code_challenge_method=s256&"
    )
