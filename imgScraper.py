import io
import asyncio
import telebot
import Scrap
import requests
import telegram
import functools
from urlmatch import urlmatch
import traceback
from time import sleep
import re

btjchat_id = 396277982
testchat_id = -447245450
# logchat_id = -436851115
logchat_id = btjchat_id
nogiblogbotToken = '1162938350:AAHSJQg4vAqmmOgrMTG9mKPiDC8lHsAM6WE'
testbotToken = '1201408151:AAGmC05wwGoAHpfgjmiO7eqCgfW0I0UlKMU'

botToken = testbotToken

bot = telebot.TeleBot(botToken, threaded=False)

bot2 = telegram.Bot(token=botToken)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}


supportList = [
    "http://blog.nogizaka46.com/*",
    "https://www.keyakizaka46.com/s/k46o/diary/detail/*",
    "https://www.hinatazaka46.com/s/official/diary/detail/*",
    "https://www.hinatazaka46.com/s/h46app/diary/detail/*",
    "https://mdpr.jp/*/detail/*",
    "https://idol.gravureprincess.date/*",
    "https://hustlepress.co.jp/*",
    "https://www.micmicidol.com/*",
    "https://www.keyakizaka46.com/s/k46o/page/portrait_hiragana_*",
    "https://natalie.mu/*/news/*",
    "https://thetv.jp/news/detail/*",
    "https://mainichikirei.jp/article/*",
    "https://archive.sakamichi.co/*/blogs/*"
]



def imgProcess(data):
    update = telebot.types.Update.de_json(data)
    # bot.send_message(logchat_id, data)
    bot.process_new_updates([update])

def sendMediaGroup(chat_id, media, timeout, reply_to_message_id):
    try:
        bot2.send_media_group(chat_id=chat_id,
                      media=media,
                      timeout=timeout,
                      reply_to_message_id=reply_to_message_id)
    except Exception as e:
        sleep(5)
        bot.send_message(btjchat_id, text=e)
        # bot.send_message(btjchat_id, text=traceback.format_exc())
        sendMediaGroup(chat_id, media, timeout, reply_to_message_id)


@bot.message_handler(func=lambda message: message.text is not None and message.text == '/s')
def handle_supportList(message):
    msg = functools.reduce(lambda txt, url: txt + "\n" + url, supportList, "Supported website:")
    bot.send_message(message.chat.id, msg,
                     reply_to_message_id=message.message_id)



@bot.message_handler(func=lambda message: message.text is not None)
def handle_message(message):
    try:
        regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
        matches = re.findall(regex, message.text)
        for rawUrl in matches:
            if not (rawUrl.startswith("https://") or rawUrl.startswith("http://")):
                rawUrl = "https://"+ message.text
            # bot.send_message(btjchat_id, text=rawUrl)
            if "hinatazaka46.com/s/h46app/" in rawUrl:
                rawUrl = rawUrl.replace("hinatazaka46.com/s/h46app", "hinatazaka46.com/s/official")
            with requests.get(rawUrl, headers=headers) as response:
                if response.status_code == 200:
                    url = requests.get(rawUrl).url
                    bot.send_message(btjchat_id, text=url)
                    result = []
                    if url.startswith("https://www.hinatazaka46.com/s/official/diary/detail/"):
                        result = asyncio.run(Scrap.hina(response.content))
                    elif url.startswith("http://blog.nogizaka46.com/") or url.startswith("https://blog.nogizaka46.com/"):
                        result = asyncio.run(Scrap.nogi(response.content))
                    elif url.startswith("https://www.keyakizaka46.com/s/k46o/diary/detail/"):
                        result = asyncio.run(Scrap.keya(response.content))
                    elif url.startswith("https://sakurazaka46.com/s/s46/diary/detail/"):
                        result = asyncio.run(Scrap.saku(response.content))
                    elif url.startswith('https://mdpr.jp/'):
                        result = asyncio.run(Scrap.mdpr(url.split("/")[-1]))
                    elif url.startswith("https://idol.gravureprincess.date/") or url.startswith("https://www.micmicidol.com/"):
                        result = asyncio.run(Scrap.idolGravDateMicMic(response.content))
                    elif url.startswith("https://hustlepress.co.jp/"):
                        result = asyncio.run(Scrap.hustlePress(response.content))
                    elif url.startswith("https://www.keyakizaka46.com/s/k46o/page/portrait_hiragana"):
                        result = asyncio.run(Scrap.portraitHiragana(response.content))
                    elif urlmatch(supportList[9], url):
                        result = asyncio.run(Scrap.natalieMu(url.split("/")[-1]))
                    elif "/".join(url.split("/")[:6]).startswith("https://thetv.jp/news/detail/"):
                        result = asyncio.run(Scrap.thetv(response.content))
                    elif url.split("?")[0].startswith("https://mainichikirei.jp/article/"):
                        with requests.get(url.split("?")[0]) as r:
                            if r.status_code == 200:
                                with requests.get(url.split("?")[0] + "?photo=001") as r2:
                                    if r2.status_code == 200:
                                        result = asyncio.run(Scrap.mainichikirei(r2.content))
                    elif urlmatch(supportList[12], url):
                        result = asyncio.run(Scrap.sakamichiArchive(response.content))
                    flat_list = [item for sublist in result for item in sublist]
                    bot.send_message(message.chat.id, f"Number of images found: {len(flat_list)}\n\nSending images...", reply_to_message_id=message.message_id)
                    for imgs in result:
                        # bot2.send_media_group(chat_id=message.chat.id,
                        #                       media=list(
                        #                           map(lambda s: telegram.InputMediaDocument(media=io.BytesIO(s)), imgs)),
                        #                       timeout=200,
                        #                       reply_to_message_id=message.message_id)
                        sendMediaGroup(chat_id=message.chat.id,
                                       media=list([telegram.InputMediaDocument(media=io.BytesIO(s),
                                                                               filename="image.jpg")
                                                   for i, s in enumerate(imgs)]),
                                       timeout=200,
                                       reply_to_message_id=message.message_id)
                    bot.send_message(message.chat.id, "Sent all images", reply_to_message_id=message.message_id)
                else:
                    bot.send_message(message.chat.id, f"Failed to reach this site", reply_to_message_id=message.message_id)
    except Exception as e:
        print(e)
        print(traceback.format_exc())



if __name__ == '__main__':
    pass