import json
import socket
import requests
from random import randint
import pyscreenshot as ImageGrab


# Written for Freestyle Gunz.
# To be used with the Freestyle MCV software.
# Written by Carter, 2016.

class Freestyle:
    """
    Opens socket server.
    Gets queried to take
    screenshots. Once
    MCV accepts runtime
    args, this will accept
    itemid queries.
    """

    def listen(self, port):
        '''Gets queries, takes screenshots.'''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to localhost with given port
        self.s.bind(('', port))
        self.s.listen(5)
        while True:
            client, addr = self.s.accept()
            data = client.recv(4096)
            d = data.split(' ')
            self.take_shot(int(d[0]), int(d[1]), int(d[2]), int(d[3]))
            print('New connection from: {}'.format(str(addr)))

    def take_shot(self, x, y, x1, y1):
        '''Takes screenshot with given coordinates.'''
        shot = ImageGrab.grab(bbox=(x, y, x1, y1))
        file_name = '{}.png'.format(str(randint(10000, 99000)))
        shot.save(file_name)
        self.archive(file_name)

    def archive(self, file_name):
        '''Uses imgsafe to store image.'''
        imgup = 'https://imgsafe.org/upload'
        image = {'files[]': open(file_name, 'rb')}
        try:
            r = requests.post(imgup, files=image)
        except:
            print('Request failed')
        print(r.text)
        log = open('log.txt', 'a+')
        data = json.loads(r.text)
        log.write('http:{}{}'.format(data['files'][0]['url'], '\n'))

screen = Freestyle()
screen.listen(250)
