import sys
import requests


def start():
    r = requests.post(
        'http://localhost:8899',
        json=[
            {"type": "nc", "port": 80},
            {"type": "http", "port": 4443, "cert": "self-signed"},
        ],
    )
    print(r.status_code)
    print(r.text)


def stop():
    r = requests.get('http://localhost:8899/clear')
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    if sys.argv[1] == 'start':
        start()
    if sys.argv[1] == 'stop':
        stop()
