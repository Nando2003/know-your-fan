import os
import asyncio
import httpx
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from services.fetch_esports_news import scrap_news

X_WEBHOOK_TOKEN = os.environ.get("X_WEBHOOK_TOKEN", "")
DJANGO_WEBHOOK = "http://django_app:8000/dashboard/webhook/"

if not X_WEBHOOK_TOKEN:
    raise ValueError("X_WEBHOOK_TOKEN environment variable is not set.")

async def scrape_and_notify():
    """
    Executa o scraping e envia a lista de notícias ao webhook Django
    num único POST com payload JSON: { "articles": [...] }.
    Força Host: localhost para que o Django aceite a requisição.
    """
    print(f"[{datetime.utcnow().isoformat()}] Iniciando scraping de notícias…")
    items = scrap_news()
    if not items:
        print("Nenhuma notícia encontrada.")
        return

    result = {"articles": items}
    
    headers = {
        "Host": "localhost",
        "X-WEBHOOK-TOKEN": X_WEBHOOK_TOKEN,
        "Content-Type": "application/json",
    }
    
    try:
        async with httpx.AsyncClient() as client:
            
            resp = await client.post(
                DJANGO_WEBHOOK,
                headers=headers,
                json=result,
                timeout=60
            )
            
            resp.raise_for_status()
            
        print(f"✔ Enviado {len(items)} artigos com sucesso.")
        
    except Exception as e:
        print(f"✖ Erro ao enviar lista de artigos: {e}")

def start_scheduler(loop):
    # Cria o scheduler vinculado ao loop
    scheduler = AsyncIOScheduler(event_loop=loop)
    trigger   = IntervalTrigger(minutes=30)

    # Agrega o job: 
    #   - executa logo de cara (next_run_time=datetime.now())
    #   - depois a cada 30min
    scheduler.add_job(
        scrape_and_notify,
        trigger=trigger,
        next_run_time=datetime.now(),
        id="news_scrape_interval",
        replace_existing=True
    )

    scheduler.start()
    print("Scheduler iniciado: primeira execução imediata e depois a cada 30 minutos.")

if __name__ == "__main__":
    # 1) Cria e seta o loop manualmente
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 2) Inicia o scheduler com a job imediata + interval
    start_scheduler(loop)

    # 3) Executa o loop
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.close()
