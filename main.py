import re

import httpx
import undetected_chromedriver as uc
import uvicorn

from typing import Union

from fastapi import FastAPI
from bs4 import BeautifulSoup

from pydantic import BaseModel

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://www.metal.com/Lithium-ion-Battery/202303240001"
LOCALHOST = True  # Make this False if you want to access remotely

# Instantiate web framework (already async)
api = FastAPI(
    title="PriceScraperToAPI",
    docs_url="/",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# httpx client (in async mode to avoid blocking the event loop)
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 "
                  "Firefox/111.0",
}
fetch = httpx.AsyncClient(headers=headers)

# Browser in headless mode. (optional, the scraper works without this as well
# using selenium=False in /price parameter)
# This use an undetected version of selenium to bypass most bot detecting
# algorithms and cloudflare
driver = uc.Chrome(headless=True)


class Response(BaseModel):
    ok: bool
    msg: str
    price: Union[float, None]


# /price endpoint handler
@api.get("/price", response_model=Response)
async def price_handler(selenium: bool = False):
    if not selenium:
        response = await fetch.get(URL)
        if response.status_code != 200:
            return {
                "ok": False,
                "msg": "Couldn't fetch the site.",
                "price": None,
            }
        html = response.text
    else:
        driver.get(URL)

        # Wait until footer is rendered (everything else we need renders
        # before this)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            'smm-component-footer-en')))
        html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    price_div = soup.find(
        "span", {
            # regex magic
            "class": re.compile(r"strong___\w+\sprice\w+")
        }
    )
    if not price_div or not price_div.text.strip():
        return {
            "ok": False,
            "msg": "Can't find the required element on the webpage",
            "price": None,
        }
    price = price_div.text.strip()

    if not price.isdigit() and not price.replace(".", "").isdigit():
        return {
            "ok": False,
            "msg": "Didn't find an integer or a float on the webpage.",
            "price": None,
        }
    return {
        "ok": True,
        "msg": "Fetched successfully.",
        "price": float(price),
    }


uvicorn.run(
    api,
    host=("127.0.0.1" if LOCALHOST else "0.0.0.0"),
    port=46575
)
