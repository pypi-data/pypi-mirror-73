from urllib.request import urlopen
import json
from time import sleep


def returnUrls(subReddit, maxNumberImgs):
    imgUrls = []
    cont = 0

    jsonUrl = "https://www.reddit.com/r/{}.json?limit=100&raw_json=1".format(subReddit)

    resp = urlopen(jsonUrl).read().decode('utf-8')

    if resp == '{"message": "Too Many Requests", "error": 429}':
        print("ERROR! Retrying...")
        sleep(2)
        return returnUrls(subReddit, maxNumberImgs)

    jsonf = json.loads(resp)

    for post in jsonf['data']['children']:
        if post['data']['post_hint'] == "image":
            imgUrls.append(post['data']['preview']['images'][0]['source']['url'])
            cont += 1
            if 0 < maxNumberImgs == cont:
                return imgUrls

    return imgUrls
