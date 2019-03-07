import requests
import json
from selenium import webdriver
from browsermobproxy import Server
import os
from tqdm import tqdm


class FirefoxDriver():
    def __init__(self):
        self.server = server = Server("browsermob-proxy/bin/browsermob-proxy")
        self.server.start()
        self.proxy = server.create_proxy()
        profile = webdriver.FirefoxProfile()
        profile.set_proxy(self.proxy.selenium_proxy())
        self.driver = webdriver.Firefox(
            firefox_profile=profile, executable_path='./driver/geckodriver')

    def getSong(self, url, id):
        self.proxy.new_har(id, options={'captureHeaders': True})
        self.driver.get(url)
        result = json.dumps(self.proxy.har, ensure_ascii=False)
        results = json.loads(result)['log']['entries']
        results = list(
            filter(lambda x: ('mp3-s1' in x['request']['url']) or '', results))
        if len(results) > 0:
            mp3_url = results[0]['request']['url']
            r = requests.get(mp3_url, allow_redirects=True)
            open(os.path.join('data/mp3', "{}.mp3".format(id)),
                 'wb').write(r.content)


if __name__ == "__main__":

    songs = json.load(open('data/songs.json', 'r'))['items']

    fd = FirefoxDriver()

    for song in songs:
        print(song['id'])
        fd.getSong('https://zingmp3.vn' + song['link'], song['id'])
