# Not really live :)
from getjson import getjson
ORIGIN       = 1594647911
INTERVAL     = 1          # Minutes between data points
num_digits = len('000000000003')
TEMPLATE_URL = "https://raw.githubusercontent.com/microprediction/badminton/master/data/game/68mins_640x360_FRAME_keypoints.json"

import time

def live():
    """ Get 'live' data from a replay of badminton game """
    k   = int((time.time() - ORIGIN) / (INTERVAL * 60))
    url = TEMPLATE_URL.replace('FRAME',str(k).zfill(num_digits))
    data = getjson(url=url)
    person = data['people'][0]
    values = [0.01*(v-200) for v in person['pose_keypoints_2d'][3:5]]
    return values


if __name__=='__main__':
    print(live())
