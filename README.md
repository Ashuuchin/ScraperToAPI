# ScraperToAPI

### Notes:
 - This implementation has support for both basic `GET` request scraping and advanced selenium scraping with anti-bot detection and cloudflare bypass.
 - Default `GET /price` will scrape the price using basic scraping and is faster.
 - And `GET /price?selenium=true` will scrape the price using selenium chromedriver.
 - All responses will have `'ok'` parameter, if `'ok'` is False, this means something went wrong during scraping, we can check the error in `'msg'` key.
 - price will be available in `price` key of response in `float` data type.
 - The default port is `46575`.

### Example response:

```json
{
  "ok": true,
  "price": 0.12,
  "msg": "Fetched successfully.",
  "used_selenium": false
}
```

### Instructions:

```bash
$ git clone https://github.com/Ashuuchin/ScraperToAPI
$ cd ScraperToAPI
$ pip install -r requirements.txt
$ python main.py
```

### Dependencies:

- Install latest version of google chrome (optional dependency)
