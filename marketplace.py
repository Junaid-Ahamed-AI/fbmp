import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep


class FbmpSpider(scrapy.Spider):
    name = "fbmp"

    def __init__(self, *args, **kwargs):
        super(FbmpSpider, self).__init__(*args, **kwargs)
        self.base_url = "https://www.facebook.com/marketplace/115461575134685/vehicles/?exact=false"

        chromedriver_path = r"C:\Users\ahame\Desktop\Rbetrage\chromedriver.exe"

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)


    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)

    def parse(self, response):
        try:
            self.driver.get(self.base_url)
            sleep(5) 

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            listings = soup.find_all("div", class_="x3ct3a4") 

            for listing in listings:
                location = listing.find("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84").text if listing.find("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84").text else "N/A"
                price = listing.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u").text if listing.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u") else "N/A"
                link = listing.find("a", href=True)["href"] if listing.find("a", href=True) else "N/A"

                yield {
                    "location": location,
                    "price": price,
                    "link": f"https://www.facebook.com{link}"
                }
        except Exception as e:
            self.logger.error(f"Error during parsing: {str(e)}")
        finally:
            self.driver.quit()

