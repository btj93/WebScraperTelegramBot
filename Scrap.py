from multiprocessing import Pool
import requests
from pyquery import PyQuery as pq
import json
import re
import telebot

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}

natalieMuPostHeaders = {
    "x-mynatalie-os": "ios",
    "accept": "*/*",
    "x-mynatalie-app-version": "1.4.9",
    "x-mynatalie-display-resolution": "3.0",
    "x-mynatalie-device-model": "iPhone12,3",
    "accept-language": "zh-Hant-HK;q=1.0, yue-Hant-HK;q=0.9, en-HK;q=0.8, ja-HK;q=0.7",
    "accept-encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
    "user-agent": "MyNatalie production/1.4.9 (mu.natalie.my; build:1.4.9.9; iOS 14.4.2) Alamofire/5.2.2",
    "x-mynatalie-os-version": "14.4.2"
}

natalieMuPostData = {
    "device_id": "b82dbf1d-de79-407e-9a8f-25a5da0c9ee1"
}


def work(url):
    if 'natalie.mu' in url:
        with requests.get(url) as response:
            if response.status_code == 200:
                    return response.content
    else:
        with requests.get(url, headers=headers) as response:
            if response.status_code == 200:
                if 'dcimg.awalker.jp' in url:
                    with requests.get(url.replace('/v/', '/i/', 1), headers=headers, cookies=response.cookies) as response2:
                        if response2.status_code == 200:
                            return response2.content
                else:
                    return response.content


async def hina(html):
    imgUrlList = []
    d = pq(html)('div.c-blog-article__text')
    for item in d.find('img[src]').items():
        if item.attr('src') != '':
            imgUrlList.append(item.attr('src'))
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]


async def nogi(html):
    imgUrlList = []
    for img in pq(html)('div.entrybody').find('img[src]').items():
        if img.closest('a[href]') and img.closest('a[href]').attr('href') != '':
            imgUrlList.append(img.closest('a[href]').attr('href'))
        elif img.attr('src') != '' and not img.closest('div.comments'):
            imgUrlList.append(img.attr('src'))
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]

async def keya(html):
    imgUrlList = []
    for img in pq(html)('div.box-article').find('img[src]').items():
        if img.attr('src') != '':
            imgUrlList.append(img.attr('src'))
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]


async def saku(html):
    imgUrlList = []
    for img in pq(html)('div.box-article').find('img[src]').items():
        if img.attr('src') != '':
            imgUrlList.append("https://sakurazaka46.com/" + img.attr('src'))
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]


async def mdpr(article_id, image_id=0):
    if article_id is not None:
        with requests.get(
                f'https://app2-mdpr.freetls.fastly.net/api/images/dialog/article?image_id={image_id}&article_id={article_id}') as response:
            if response.status_code == 200:
                js = json.loads(response.content)
                imgUrlList = list(map(lambda o: o['url'], js['list']))
                with Pool() as pool:
                    imgList = pool.map(work, imgUrlList)
                return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]
    return []


async def idolGravDateMicMic(html):
    imgUrlList = []
    for img in pq(html)('div.post-body').find('img[src][data-original-height][data-original-width]').items():
        if img.attr("src") is not None and int(img.attr("data-original-height")) > 450 and int(
                img.attr("data-original-width")) > 450:
            imgUrl = re.sub(r'/[s,w]\d+/', "/w15000/" , str(img.attr('src')))
            imgUrlList.append(imgUrl)
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]


async def hustlePress(html):
    imgUrlList = []
    for img in pq(html)('div.entry-content').find('a[rel]').items():
        if img.attr("href") is not None and "lightbox" in img.attr("rel"):
            imgUrlList.append(img.attr("href"))
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]

bot = telebot.TeleBot('1201408151:AAGmC05wwGoAHpfgjmiO7eqCgfW0I0UlKMU', threaded=False)

async def portraitHiragana(html):
    imgUrlList = []
    for img in pq(html)('div.portrait-list-in').find('img[src]').items():
        if img.attr("src") is not None:
            imgUrlList.append(str(img.attr("src")).rsplit("/", 1)[0] + "/9999_9999_9999999.jpg")
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]


async def natalieMu(article_id):
    if article_id is not None:
        with requests.post('https://myapi.natalie.mu/v3/login/device', headers=natalieMuPostHeaders,
                           json=natalieMuPostData) as r:
            if r.status_code == 201:
                token = json.loads(r.content)['data']['access_token']
                natalieMuGetHeaders = {
                    "x-mynatalie-os": "ios",
                    "accept": "*/*",
                    "x-mynatalie-app-version": "1.4.9",
                    "x-mynatalie-display-resolution": "3.0",
                    "accept-encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
                    "x-mynatalie-device-model": "iPhone12,3",
                    "accept-language": "zh-Hant-HK;q=1.0, yue-Hant-HK;q=0.9, en-HK;q=0.8, ja-HK;q=0.7",
                    "user-agent": "MyNatalie production/1.4.9 (mu.natalie.my; build:1.4.9.9; iOS 14.4.2) Alamofire/5.2.2",
                    "x-mynatalie-token": token,
                    "x-mynatalie-os-version": "14.4.2"
                }
                with requests.get(f'https://myapi.natalie.mu/v3/news/showWithOffshot/{article_id}',
                                  headers=natalieMuGetHeaders) as response:
                    if response.status_code == 200:
                        imgUrlList = list(
                            map(lambda img: img['image'].replace('_fixw_750_lt', '').replace('cdnx', 'ogre'),
                                json.loads(response.content)['data']['gallery']))
                        with Pool() as pool:
                            imgList = pool.map(work, imgUrlList)
                        return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]



async def thetv(html):
    q = pq(html)
    imgUrlList = list(map(lambda item: re.search(r'\((.*?)\)', item.attr("style")).group(1).split("?")[0],
                          q.find("div.newsimage").find("li.thumblist__item").find("a").items()))
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]


def mwork(url):
    s = 8
    c = None
    response3 = requests.get(url.replace("thumb", f"size{s}"))
    while response3.status_code == 200:
        s += 1
        c = response3.content
        response3 = requests.get(url.replace("thumb", f"size{s}"))
    if c is not None:
        return c

async def mainichikirei(html):
    p = pq(html)
    imgUrlList = list(map(lambda photo: photo.attr("src"),
                          p.find("div.photo__photolist--inner > a[data-photo_num] > img[src]").items()))
    with Pool() as pool:
        imgList = pool.map(mwork, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]


async def sakamichiArchive(html):
    p = pq(html)
    imgUrlList = []
    for img in p.find("section.blog-view__blog__content").find("img[src]").items():
        imgUrlList.append(f'https://archive.sakamichi.co{img.attr("src")}')
    with Pool() as pool:
        imgList = pool.map(work, imgUrlList)
    return [imgList[i:i + 10] for i in range(0, len(imgList), 10)]