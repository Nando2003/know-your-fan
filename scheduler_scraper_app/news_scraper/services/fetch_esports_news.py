import json
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin


DUST2_URL = "https://www.dust2.com.br"
VALORANT_ZONE_URL = "https://valorantzone.gg"
MAIS_ESPORTES_URL = "https://maisesports.com.br/league-of-legends/"


def scrap_news() -> list[dict]:
    return scrap_mais_esportes() + scrap_valorant_zone() + scrap_dust2()


def scrap_valorant_zone():
    resp = httpx.get(VALORANT_ZONE_URL)

    if resp.status_code != 200:
        return []
    
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = []
    for art in soup.select('article.post-layout'):
        # Título e link
        a = art.select_one('h3.entry-title a.title-text')
        title = a.get_text(strip=True) # type: ignore
        href  = a['href'] # type: ignore

        url = href if href.startswith(("http://", "https://")) else urljoin(VALORANT_ZONE_URL, href) # type: ignore

        # Data
        date_span = art.select_one('.meta-item.meta-date .info-text')
        date_text = date_span.get_text(strip=True) if date_span else None

        # Imagem
        img_tag = art.select_one('.entry-thumbnail img')
        image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

        # Descrição
        desc_tag = art.select_one('.entry-excerpt')
        description = desc_tag.get_text(strip=True) if desc_tag else None

        results.append({
            'date':        date_text,
            'url':         url,
            'title':       title,
            'image_url':   image_url,
            'description': description
        })

    return results


def scrap_dust2():
    """
    Scrape Dust2.com.br, garantindo que o título
    seja sempre extraído da <div class="news-item-header">.
    """
    resp = httpx.get(DUST2_URL)
    if resp.status_code != 200:
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    results = []

    for tag in soup.find_all('a', class_=lambda c: c and ('article' in c or 'news-item' in c)):
        href = tag.get('href')
        if not href:
            continue

        # Garante URL absoluta
        url = href if href.startswith(("http://", "https://")) else urljoin(DUST2_URL, href)

        # Título: sempre dentro de .news-item-header
        header = tag.select_one('.news-item-header')
        title = header.get_text(strip=True) if header else None

        # Data
        date_el   = tag.select_one('.news-item-time, .info-text')
        date_text = date_el.get_text(strip=True) if date_el else None

        # Imagem
        img       = tag.select_one('img')
        image_url = img.get('src') if img and img.has_attr('src') else None

        # Não há descrição nos blocos <a>
        description = None

        results.append({
            'date':        date_text,
            'url':         url,
            'title':       title,
            'image_url':   image_url,
            'description': description
        })

    return results


def scrap_mais_esportes():
    resp = httpx.get(MAIS_ESPORTES_URL)
    
    if resp.status_code != 200:
        return []
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    script = soup.find('script', id="__NEXT_DATA__")
    data = json.loads(script.string) # type: ignore

    posts = data['props']['pageProps']['posts']['posts']
    articles = []
    for p in posts:
        date = p.get('date')  # ex: "2025-05-04T18:41:42"
        title = p.get('title')
        slug = p.get('slug')
        # Reconstrói a URL completa
        url = f"https://noticias.maisesports.com.br/{slug}"
        # URL da imagem principal
        image_url = p.get('featuredImage', {}).get('mainNews')
        # Resumo/texto
        description = p.get('resumed')

        articles.append({
            'date':        date,
            'url':         url,
            'title':       title,
            'image_url':   image_url,
            'description': description
        })
        
    return articles
