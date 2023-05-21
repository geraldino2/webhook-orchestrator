from flask import Flask, request
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

CFG_STREAM = open("cfg.yml", "r")
cfg = load(CFG_STREAM, Loader=Loader)

app = Flask(__name__)

@app.route("/<path>", methods=["POST"])
def webhook(path):
    if (request.method == "POST"):
        for hook in cfg["webhooks"]:
            if (hook["path"] == path):
                return ("received")
    return (b"")

app.run(host=cfg["hostname"], port=cfg["port"], debug=True)