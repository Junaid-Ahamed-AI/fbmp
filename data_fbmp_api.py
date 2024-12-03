from fastapi import FastAPI
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

app = FastAPI()

@app.get("/scrape_facebook_marketplace")
def scrape_facebook_marketplace():
    try:
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'data_fbmp.settings')
        process = CrawlerProcess(get_project_settings())
        process.crawl("fbmp") 
        process.start() 

        return {"status": "success", "message": "Scraping completed!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

