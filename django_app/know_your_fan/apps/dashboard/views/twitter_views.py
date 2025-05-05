import httpx
import secrets
import hashlib
import base64
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse

def make_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return code_verifier, code_challenge

def twitter_login(request):
    verifier, challenge = make_pkce_pair()
    request.session["twitter_pkce_verifier"] = verifier

    params = {
        "response_type":         "code",
        "client_id":             settings.TWITTER_OAUTH2_CLIENT_ID,
        "redirect_uri":          settings.TWITTER_REDIRECT_URI,
        "scope":                 settings.TWITTER_OAUTH2_SCOPES,
        "state":                 secrets.token_urlsafe(16),
        "code_challenge":        challenge,
        "code_challenge_method": "S256",
    }
    url = "https://twitter.com/i/oauth2/authorize?" + urlencode(params)
    return redirect(url)

def twitter_callback(request):
    """
    Recebe o `code` do Twitter, troca pelo access_token via OAuth2.0 + PKCE
    e o guarda na sessão para uso no formulário.
    """
    code = request.GET.get("code")
    _ = request.GET.get("state")
    verifier = request.session.pop("twitter_pkce_verifier", None)

    if not code or not verifier:
        return render(request, "dashboard/error.html", {
            "message": "Parâmetros inválidos no callback do Twitter."
        })

    # Monta o Basic Auth com Client ID/Secret
    basic = base64.b64encode(
        f"{settings.TWITTER_OAUTH2_CLIENT_ID}:{settings.TWITTER_OAUTH2_CLIENT_SECRET}".encode()
    ).decode()

    token_url = "https://api.twitter.com/2/oauth2/token"
    
    data = {
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  settings.TWITTER_REDIRECT_URI,
        "code_verifier": verifier,
    }
    headers = {
        "Authorization": f"Basic {basic}",
        "Content-Type":  "application/x-www-form-urlencoded",
    }

    resp = httpx.post(token_url, data=urlencode(data), headers=headers) # type: ignore
    if resp.status_code != 200:
        return render(request, "dashboard/error.html", {
            "message": f"Erro ao trocar código por token: {resp.text}"
        })

    token_data = resp.json()
    
    request.session["twitter_refresh_token"] = token_data.get("refresh_token")
    request.session["twitter_oauth2_access_token"] = token_data["access_token"]

    # fecha a popup e recarrega a janela pai
    return render(request, "dashboard/oauth_close_popup.html")

def twitter_ready(request):
    """
    Endpoint polled pelo JS: retorna {"ready": True, access_token: "..."}
    assim que o usuário concluir o login e obtivermos o token.
    """
    token = request.session.get("twitter_oauth2_access_token")
    if not token:
        return JsonResponse({"ready": False})

    return JsonResponse({
        "ready":        True,
        "access_token": token,
    })