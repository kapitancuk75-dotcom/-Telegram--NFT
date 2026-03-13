import asyncio
import requests

from telethon import TelegramClient

from config import API_ID, API_HASH, BOT_TOKEN, CHAT_ID, MAX_PRICE
from markets import MARKETS
from parser import parse_nft


client = TelegramClient("session", API_ID, API_HASH)

seen = set()


def send_bot_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }

    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Ошибка отправки:", e)


async def scan():

    while True:

        for market in MARKETS:

            try:

                async for msg in client.iter_messages(market, limit=30):

                    if not msg.text:
                        continue

                    if msg.id in seen:
                        continue

                    seen.add(msg.id)

                    name, price, url = parse_nft(msg.text)

                    if not name or not price:
                        continue

                    if price > MAX_PRICE:
                        continue

                    message = (
                        f"🎁 Найден NFT подарок\n\n"
                        f"Название: {name}\n"
                        f"Цена: {price} TON\n\n"
                        f"🔗 Открыть:\n{url if url else 'нет ссылки'}"
                    )

                    send_bot_message(message)

            except Exception as e:

                print("Ошибка сканирования", market, e)

        await asyncio.sleep(20)


async def main():

    print("NFT scanner started")

    await scan()


with client:
    client.loop.run_until_complete(main())
