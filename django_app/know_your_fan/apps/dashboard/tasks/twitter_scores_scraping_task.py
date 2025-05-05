import time
import httpx
from typing import List, Dict, Any, Optional

from celery import shared_task
from apps.dashboard.models.dashboard_model import Dashboard
from apps.dashboard.models.fan_profile_model import FanProfile


BASE = "https://api.twitter.com/2"


def _get(url: str,
         token: str,
         params: dict,
         max_retries: int = 5,
         initial_backoff: float = 1.0
         ) -> dict:
    """
    Faz GET com retries em HTTP 429 e 5xx, usando back‑off exponencial.
    """
    headers = {"Authorization": f"Bearer {token}"}
    backoff = initial_backoff

    for attempt in range(1, max_retries + 1):
        try:
            resp = httpx.get(url, headers=headers, params=params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            # retry only on 429 or 5xx
            if status == 429:
                reset = e.response.headers.get("x-rate-limit-reset")
                if reset and reset.isdigit():
                    sleep_for = max(int(reset) - int(time.time()) + 1, backoff)
                else:
                    sleep_for = backoff
            elif 500 <= status < 600:
                sleep_for = backoff
            else:
                # erro client não recuperável
                raise
            # log e dorme
            print(f"[{status}] attempt {attempt}/{max_retries}, retrying in {sleep_for:.1f}s…")
            time.sleep(sleep_for)
            backoff *= 2

    raise RuntimeError(f"Failed to GET {url} after {max_retries} attempts")


def get_user_tweets_with_refs(user_id: str,
                              token: str,
                              max_results: int = 5,
                              pagination_token: Optional[str] = None
                              ) -> dict:
    """
    Timeline do usuário (inclui tweets originais e retweets),
    com 'referenced_tweets' para sabermos qual tipo cada um é.
    """
    url = f"{BASE}/users/{user_id}/tweets"
    params = {
        "max_results": max_results,
        "tweet.fields": "id,created_at,text,referenced_tweets,public_metrics",
        # precisamos do author_id dos tweets referenciados para filtrar Retweets
        "expansions": "referenced_tweets.id.author_id",
        "user.fields": "id,username"
    }
    if pagination_token:
        params["pagination_token"] = pagination_token
    return _get(url, token, params)


def retweets_of_org(user_id: str, org_id: str, token: str, max_results: int = 100) -> List[Dict[str, Any]]:
    """
    Retorna até max_results retweets que o usuário fez de tweets da Org.
    """
    data = get_user_tweets_with_refs(user_id, token, max_results)
    tweets    = data.get("data", [])
    includes  = data.get("includes", {})
    # mapeia referenced tweet id → seu author_id
    ref_map = {
        rt["id"]: rt_author
        for rt in includes.get("tweets", [])
        for rt_author in [rt.get("author_id")]
    }
    retweets = []
    for t in tweets:
        for ref in t.get("referenced_tweets", []):
            if ref["type"] == "retweeted" and ref_map.get(ref["id"]) == org_id:
                retweets.append(t)
    return retweets


def replies_to_org(user_id: str, org_id: str, token: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Retorna até max_results menções (respostas) do usuário à Org.
    """
    url = f"{BASE}/users/{user_id}/mentions"
    params = {
        "max_results": max_results,
        "tweet.fields": "id,created_at,text,referenced_tweets,public_metrics",
        "expansions": "referenced_tweets.id.author_id",
        "user.fields": "id,username"
    }
    data = _get(url, token, params)
    tweets   = data.get("data", [])
    includes = data.get("includes", {})
    ref_map = {rt["id"]: rt.get("author_id") for rt in includes.get("tweets", [])}
    replies = []
    for t in tweets:
        for ref in t.get("referenced_tweets", []):
            if ref["type"] == "replied_to" and ref_map.get(ref["id"]) == org_id:
                replies.append(t)
    return replies


def liked_tweets_of_org(user_id: str, org_id: str, token: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Retorna até max_results tweets curtidos pelo usuário
    cujo author_id seja da Org.
    """
    url = f"{BASE}/users/{user_id}/liked_tweets"
    params = {
        "max_results": max_results,
        "tweet.fields": "id,created_at,text,author_id,public_metrics"
    }
    data = _get(url, token, params)
    return [t for t in data.get("data", []) if t.get("author_id") == org_id]


@shared_task(max_retries=5)
def update_dashboard_twitter(self, dashboard_id: int, access_token: str):
    try:
        try:
            dash = Dashboard.objects.get(pk=dashboard_id)
        except Dashboard.DoesNotExist:
            return 1
        
        fp: FanProfile = dash.fan_profile
        team = fp.org_preference
        
        org_username = team.x_account.rstrip('/').split('/')[-1]
        
        me = _get(f"{BASE}/users/me", access_token, {})
        me_id = me["data"]["id"]
        
        org = _get(f"{BASE}/users/by/username/{org_username}", access_token, {})
        org_id = org["data"]["id"]
        
        rt_list = retweets_of_org(me_id, org_id, access_token, max_results=50)
        rep_list = replies_to_org(me_id, org_id, access_token, max_results=50)
        like_list = liked_tweets_of_org(me_id, org_id, access_token, max_results=50)
        
        fp.rt_org_posts = len(rt_list)
        fp.interacted_org_posts = len(rep_list)
        fp.liked_org_posts = len(like_list)
        fp.save(update_fields=['rt_org_posts','liked_org_posts','interacted_org_posts'])
        
        dash.twitter_status = 'finished'
        dash.save(update_fields=['twitter_status'])
        
    except Exception as exc:
        print(f"[update_dashboard_twitter] erro no Dashboard {dashboard_id}: {exc}")
        update_dashboard_twitter.retry(exc=exc, countdown=60) # type: ignore

        