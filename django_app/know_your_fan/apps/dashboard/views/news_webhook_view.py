import json
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.dashboard.models.esports_news_model import ESportsNews


@csrf_exempt
@require_POST
def news_webhook_view(request: HttpRequest) -> JsonResponse: 
    try:
        data = json.loads(request.body)
        
        articles = data.get("articles", [])
        
        if not articles:
            return JsonResponse({"error": "Nenhum artigo encontrado"}, status=400)
        
        for article in articles:
            
            date = article.get("date")
            url = article.get("url")
            title = article.get("title")
            image_url = article.get("image_url")
            description = article.get("description")
            
            if not (url and title):
                continue
            
            if ESportsNews.objects.filter(Q(source=url)).exists():
                continue
            
            news = ESportsNews(
                title=title,
                source=url,
                image_url=image_url,
                description=description,
                published_at=date
            )
            
            news.full_clean()
            news.save()
        
        return JsonResponse({"status": "success"}, status=200)
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return JsonResponse({"error": str(e)}, status=400)