from datetime import timedelta
from urllib.parse import urlparse
from random import sample
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from celery import shared_task
from django.utils import timezone

from apps.dashboard.models import Dashboard, ESportsNews

def compute_semantic_score(profile_terms, doc_texts):
    profile_doc = " ".join(profile_terms)
    corpus = [profile_doc] + doc_texts
    tfidf = TfidfVectorizer().fit_transform(corpus)
    return cosine_similarity(tfidf[0:1], tfidf[1:]).flatten().tolist()

@shared_task
def recommend_news_for_dashboard(dashboard_id: int):
    try:
        dashboard = Dashboard.objects.get(pk=dashboard_id)
    except Dashboard.DoesNotExist:
        return 1

    fp = dashboard.fan_profile
    org = fp.org_preference.name.lower()
    games = [g.name.lower() for g in fp.games.all()]

    cutoff = timezone.now() - timedelta(days=7)
    recent_news = ESportsNews.objects.filter(created_at__gte=cutoff)

    docs = []
    metas = []
    for news in recent_news:
        text = f"{news.title} {news.description or ''}".strip().lower()
        docs.append(text)
        metas.append(news)

    profile_terms = [org] + games
    semantic_scores = compute_semantic_score(profile_terms, docs)

    scored = []
    for idx, news in enumerate(metas):
        score = semantic_scores[idx] * 10
        text = docs[idx]

        # bonus points
        if org in text:
            score += 5
        for game in games:
            if game in text:
                score += 3

        domain = urlparse(news.source).netloc.lower()
        if "dust2.com.br" in domain and any("cs2" in g for g in games):
            score += 2
        if "valorantzone.gg" in domain and any("valorant" in g for g in games):
            score += 2
        if "maisesports.com.br" in domain and any("lol" in g for g in games):
            score += 2

        scored.append((score, news, docs[idx]))

    # separar notícias para org e para jogos
    org_list = [ (s, n) for s, n, txt in scored if org in txt ]
    games_list = [ (s, n) for s, n, txt in scored if any(game in txt for game in games) ]

    # ordenar por score desc
    org_list.sort(key=lambda x: x[0], reverse=True)
    games_list.sort(key=lambda x: x[0], reverse=True)

    # selecionar top pools
    top_org_pool = [n for _, n in org_list[:10]]  # top 10 para randomizar
    top_games_pool = [n for _, n in games_list[:10]]

    # escolher aleatoriamente 3 para org e 2 para jogos
    chosen_org = sample(top_org_pool, k=min(3, len(top_org_pool)))
    chosen_games = sample(top_games_pool, k=min(2, len(top_games_pool)))

    # combinar, evitando duplicatas
    chosen = []
    for news in chosen_org + chosen_games:
        if news not in chosen:
            chosen.append(news)

    # atualizar dashboard
    dashboard.news.clear()
    for news in chosen:
        dashboard.news.add(news)

    dashboard.news_status = 'finished'
    dashboard.save()
