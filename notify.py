import requests

from config import GITTER_WEBHOOK


def gitter(label, counter):
    if GITTER_WEBHOOK is None:
        return

    payload = {'message': '*{}* migration counter: *{}*'.format(label, counter)}
    requests.post(GITTER_WEBHOOK, data=payload)
