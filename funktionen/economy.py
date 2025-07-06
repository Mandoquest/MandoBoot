import json
import os

PFAD = "data/konten.json"
os.makedirs("data", exist_ok=True)

def lade_konten():
    if not os.path.exists(PFAD):
        return {}
    with open(PFAD, "r") as f:
        return json.load(f)

def speichere_konten(daten):
    with open(PFAD, "w") as f:
        json.dump(daten, f, indent=2)

_konten = lade_konten()

def gib_guthaben(uid):
    uid = str(uid)
    if uid not in _konten:
        _konten[uid] = 1000
        speichere_konten(_konten)
    return _konten[uid]

def ändere_guthaben(uid, betrag):
    uid = str(uid)
    _konten[uid] = gib_guthaben(uid) + betrag
    speichere_konten(_konten)