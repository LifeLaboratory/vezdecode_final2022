from requests import get, post
import string
import random

char = string.ascii_uppercase + string.digits + string.ascii_lowercase
HOST, PORT = '89.208.198.171', '13452'


def post_image():
    fp = open('1.jpeg', 'rb')
    # files = {'image': fp.read(), 'text_up': 'hello', 'text_down': 'world!'}
    # files = {'image': fp.read()}
    # files = {'text_up': 'hello', 'text_down': 'world!'}
    files = {}
    data = {'image': fp, 'text_up': 'hello', 'text_down': 'world!'}
    resp = post(f'http://{HOST}:{PORT}/set', data=files)
    fp.close()


def post_image_param(image, text_up, text_down):
    fp = open(f'{image}.jpeg', 'rb')
    files = {'image': fp.read(), 'text_up': text_up, 'text_down': text_down}
    data = {'image': fp, 'text_up': 'hello', 'text_down': 'world!'}
    resp = post(f'http://{HOST}:{PORT}/set', data=files)
    print(resp.text)
    fp.close()


def get_image():
    img = get(f'http://{HOST}:{PORT}/get/1')


text_up = ['ttt1', 'help2', 'hhhhh', 'rtweqtr', 'wetwt', 'twtqtqw', 'qwre qwe', 'fas fasf', 'gv sv xvs df', 'r43242', '234 234 243 234']

for i in range(100):
    post_image_param(random.randint(1, 7), random.choice(text_up), random.choice(text_up))