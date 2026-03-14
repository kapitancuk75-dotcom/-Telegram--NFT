import re

def parse_nft(text):
    name = None
    price = None
    url = None

    name_match = re.search(r'([A-Za-z ]+ #\d+)', text)
    if name_match:
        name = name_match.group(1)

    price_match = re.search(r'(\d+(\.\d+)?)\s?TON', text)
    if price_match:
        price = float(price_match.group(1))

    url_match = re.search(r'(https://t.me/\S+)', text)
    if url_match:
        url = url_match.group(1)

    return name, price, url
