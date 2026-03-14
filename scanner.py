import asyncio
import requests
from telethon import TelegramClient
from parser import parse_nft
from config import API_ID, API_HASH, BOT_TOKEN, CHAT_ID, MAX_PRICE
from markets import MARKETS

# Telethon client (использует session.session)
client = TelegramClient("session", API_ID, API_HASH)

seen = set()  # чтобы не дублировать сообщения

# функция отправки уведомлений через Telegram-бота
def send_bot_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, data=data)
        if not response.ok:
            print("Ошибка отправки:", response.text)
    except Exception as e:
        print("Ошибка отправки:", e)

# основной цикл сканера
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
                        f"Цена: {price} TON\n"
                        f"🔗 Ссылка: {url if url else 'нет ссылки'}"
                    )
                    send_bot_message(message)

            except Exception as e:
                print(f"Ошибка сканирования {market}: {e}")

        await asyncio.sleep(20)

# точка входа
async def main():
    print("NFT scanner started")
    send_bot_message("🚀 NFT сканер запущен и работает!")
    await scan()

with client:
    client.loop.run_until_complete(main())
