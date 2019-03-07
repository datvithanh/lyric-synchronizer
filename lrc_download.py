import requests
import json
import os

songs = json.load(open('data/songs.json', 'r'))['items']
ids = list(map(lambda x: x[:-4], os.listdir('data/mp3')))
for song in songs:
    if song['id'] in ids:
        if len(song['lyric']) > 0:
            r = requests.get(song['lyric'])
            open(os.path.join('data/lrc', "{}.lrc".format(song['id'])),
                    'wb').write(r.content)
        else:
            print(song['id'])