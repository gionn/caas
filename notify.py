import requests
import threading

from config import GITTER_WEBHOOK, SLACK_WEBHOOK


def notify_all(label, counter):
    threads = []

    gitter = threading.Thread(target=_gitter, args=(label, counter))
    threads.append(gitter)

    slack = threading.Thread(target=_slack, args=(label, counter))
    threads.append(slack)

    for thread in threads:
        thread.setDaemon(True)
        thread.start()


def _gitter(label, counter):
    if GITTER_WEBHOOK is None:
        return

    payload = {'message': '*{}* migration counter: *{}*'.format(label, counter)}
    requests.post(GITTER_WEBHOOK, data=payload)


def _slack(label, counter):
    if SLACK_WEBHOOK is None:
        return

    payload = {'text': '_*{}* migration counter: *{}*_'.format(label, counter)}
    requests.post(SLACK_WEBHOOK, json=payload)
