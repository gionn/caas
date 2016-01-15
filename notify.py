import requests
import threading

from config import GITTER_WEBHOOK


def notify_all(label, counter):
    t = threading.Thread(target=_gitter, args=(label, counter))
    t.setDaemon(True)
    t.start()


def _gitter(label, counter):
    if GITTER_WEBHOOK is None:
        return

    payload = {'message': '*{}* migration counter: *{}*'.format(label, counter)}
    requests.post(GITTER_WEBHOOK, data=payload)
