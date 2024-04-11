from flask import Flask
from flask import request
from ltf2.util.config import get_ltfrc_section

from ltf2.console_app.exposure.exposure import NcExposure, HttpExposure


app = Flask(__name__)

EXPOSURES = []


def handle_post_data(json_data):
    if not isinstance(json_data, list):
        return "JSON must be list of dicts/objects", 400
    for e in json_data:
        if e['type'].lower() == 'nc':
            EXPOSURES.append(NcExposure(e['port']))
        elif e['type'].lower() == 'http':
            EXPOSURES.append(HttpExposure(e['port'], tls=e['cert']))
    [x.start() for x in EXPOSURES if not x.handle]
    return [repr(x) for x in EXPOSURES]


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return [repr(x) for x in EXPOSURES]
    if request.method == 'POST':
        post_data = request.get_json(force=True)
        return handle_post_data(post_data)


@app.route('/clear')
def clear():
    for e in EXPOSURES:
        e.stop()
    EXPOSURES.clear()
    return EXPOSURES


def main():
    port = int(get_ltfrc_section("edgio-console-app")['exposure_service_port'])
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
