from telethon import TelegramClient, events
from credentails import telegram_api_hash, telegram_api_id
from binance_api import BinanceAPI
import re

client = TelegramClient('anon', telegram_api_id, telegram_api_hash)
user_input_channel = "https://t.me/TodayWePush"
binance = BinanceAPI()
print("> Waiting for Trigger...")


@client.on(events.NewMessage(chats=user_input_channel))
async def new_message_listener(event):
    new_message = event.message.message
    print(len(str(new_message)))
    slug = "https://www.binance.com/en/trade/"
    if new_message.find(slug):
        url = re.findall('(?P<url>https?://[^\s]+)', new_message)
        trade_pair = new_message.split(slug)[-1]
        asset = trade_pair.split("_")[0]
        quote = trade_pair.split("_")[1]
        print("> Selected Pair: {}".format(trade_pair))
        binance.start_session(asset, quote)
    print(new_message)


with client:
    client.run_until_disconnected()
