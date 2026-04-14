import aiohttp
import asyncio
from bs4 import BeautifulSoup
import ssl
import certifi
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler('logs/app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def scrape_site(session, url):
    try:
        async with session.get(url, timeout=10) as res:
            text = await res.text()
            soup = BeautifulSoup(text, "html.parser")

            articles = []
            for item in soup.find_all("article"):
                title = item.find("h2")
                content = item.find_all("p")

                articles.append({
                    "title": title.text.strip() if title else "",
                    "content": " ".join([p.text.strip() for p in content])
                })

            logger.info(f"Scraped {len(articles)} articles from {url}")

            return articles

    except Exception as e:
        logger.error(f"Error in {url}: {e}")
        return []


async def run_crawler(urls):
    
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [scrape_site(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        all_articles = [item for sublist in results for item in sublist]
        logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles