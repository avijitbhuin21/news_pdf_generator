import aiohttp
import re
import html
import asyncio
import random
import nest_asyncio
nest_asyncio.apply()  # Apply nest_asyncio to allow nested event loops

async def get_bbc_news_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://feeds.bbci.co.uk/news/world/rss.xml') as response:
            text = await response.text()
            pattern = re.compile(r"<item>.*?</item>", re.DOTALL)
            xml_contents = pattern.findall(text)[:5]
            mm = []
            for xml_content in xml_contents:            
                mm.append({
                        'title': html.unescape(re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', xml_content).group(1)),
                        'description': html.unescape(re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', xml_content).group(1)),
                        'link': re.search(r'<link>(.*?)</link>', xml_content).group(1),
                        'pub_date': re.search(r'<pubDate>(.*?)</pubDate>', xml_content).group(1).split(', ')[1][:11],
                        'media_url': re.search(r'<media:thumbnail width="(\d+)" height="(\d+)" url="(.*?)"/>', xml_content).group(3) if re.search(r'<media:thumbnail width="(\d+)" height="(\d+)" url="(.*?)"/>', xml_content) else None,
                        'platform': 'BBC News',
                    })
            return mm

async def get_nyt_news_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml') as response:
            text = await response.text()
            pattern = re.compile(r"<item>.*?</item>", re.DOTALL)
            xml_contents = pattern.findall(text)[:5]
            mm = []
            for xml_content in xml_contents:
                mm.append({
                    'title': html.unescape(re.search(r'<title>(.*?)</title>', xml_content).group(1)) if re.search(r'<title>(.*?)</title>', xml_content) else None,
                    'description': html.unescape(re.search(r'<description>(.*?)</description>', xml_content).group(1)) if re.search(r'<description>(.*?)</description>', xml_content) else None,
                    'link': re.search(r'<link>(.*?)</link>', xml_content).group(1) if re.search(r'<link>(.*?)</link>', xml_content) else None,
                    'pub_date': re.search(r'<pubDate>(.*?)</pubDate>', xml_content).group(1).split(', ')[1][:11] if re.search(r'<pubDate>(.*?)</pubDate>', xml_content) else None,
                    'media_url': re.search(r'<media:content.*?url="(.*?)"', xml_content).group(1) if re.search(r'<media:content.*?url="(.*?)"', xml_content) else None,
                    'platform': 'New York Times',
                })
            return mm

async def get_nbc_news_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://feeds.nbcnews.com/nbcnews/public/news') as response:
            text = await response.text()
            pattern = re.compile(r"<item>.*?</item>", re.DOTALL)
            xml_contents = pattern.findall(text)[:5]
            mm = []
            for xml_content in xml_contents:
                mm.append({
                    'title': html.unescape(re.search(r'<title>(.*?)</title>', xml_content).group(1)) if re.search(r'<title>(.*?)</title>', xml_content) else None,
                    'description': html.unescape(re.search(r'<description>(.*?)</description>', xml_content).group(1)) if re.search(r'<description>(.*?)</description>', xml_content) else None,
                    'link': re.search(r'<link>(.*?)</link>', xml_content).group(1) if re.search(r'<link>(.*?)</link>', xml_content) else None,
                    'pub_date': re.search(r'<pubDate>(.*?)</pubDate>', xml_content).group(1).split(', ')[1][:11] if re.search(r'<pubDate>(.*?)</pubDate>', xml_content) else None,
                    'media_url': re.search(r'<media:thumbnail url="(.*?)"', xml_content).group(1) if re.search(r'<media:thumbnail url="(.*?)"', xml_content) else (re.search(r'<media:content url="(.*?)"', xml_content).group(1) if re.search(r'<media:content url="(.*?)"', xml_content) else None),
                    'platform': 'NBC News',
                })
            return mm

async def get_ndtv_news_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://feeds.feedburner.com/ndtvnews-top-stories') as response:
            text = await response.text()
            pattern = re.compile(r"<item>.*?</item>", re.DOTALL)
            xml_contents = pattern.findall(text)[:5]
            mm = []
            for xml_content in xml_contents:
                mm.append({
                    'title': html.unescape(re.search(r'<title>\s*<!\[CDATA\[\s*(.*?)\s*\]\]>\s*</title>', xml_content).group(1)) if re.search(r'<title>\s*<!\[CDATA\[\s*(.*?)\s*\]\]>\s*</title>', xml_content) else None,
                    'description': html.unescape(re.search(r'<description>\s*<!\[CDATA\[\s*(.*?)\s*\]\]>\s*</description>', xml_content).group(1)) if re.search(r'<description>\s*<!\[CDATA\[\s*(.*?)\s*\]\]>\s*</description>', xml_content) else None,
                    'link': html.unescape(re.search(r'<link>\s*<!\[CDATA\[\s*(.*?)\s*\]\]>\s*</link>', xml_content).group(1)) if re.search(r'<link>\s*<!\[CDATA\[\s*(.*?)\s*\]\]>\s*</link>', xml_content) else None,
                    'pub_date': re.search(r'<pubDate><!\[CDATA\[(.*?)]]></pubDate>', xml_content).group(1).split(', ')[1][:11] if re.search(r'<pubDate><!\[CDATA\[(.*?)]]></pubDate>', xml_content) else None,
                    'media_url': re.search(r'<media:content url="(.*?)"', xml_content).group(1) if re.search(r'<media:content url="(.*?)"', xml_content) else None,
                    'platform': 'NDTV News',
                })
            return mm



async def get_trending_news_async():
    tasks = [
        get_bbc_news_async(),
        get_nyt_news_async(),
        get_nbc_news_async(),
        get_ndtv_news_async()
    ]
    random.shuffle(tasks)
    results = await asyncio.gather(*tasks)
    results = [item for sublist in results for item in sublist if isinstance(sublist, list)]
    return results

def get_trending_news():
    try:
        # loop = asyncio.get_running_loop()
        return asyncio.run(get_trending_news_async())
    except RuntimeError:
        return asyncio.run(get_trending_news_async())

