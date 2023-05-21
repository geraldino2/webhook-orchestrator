import os, hashlib, hmac

from flask import Flask, request
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

CFG_STREAM = open("cfg.yml", "r")
cfg = load(CFG_STREAM, Loader=Loader)

app = Flask(__name__)

def exec_os_trigger(trigger: str) -> None:
    return None

def verify_gh_signature(request: request, secret: str) -> bool:
    if "x-hub-signature-256" not in request.headers:
        return False
    signature_header = request.headers["x-hub-signature-256"]
    hash_object = hmac.new(
        secret.encode("utf-8"),
        msg=request.data, digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        return False
    return True

def validate_request(hook: dict, request: request) -> bool:    
    if (hook["type"] == "github" and hook["secret"] != ""):
        secret_token = os.environ.get(hook["secret"])
        if(not verify_gh_signature(request, secret_token)):
            return False
    exec_os_trigger(hook["trigger"])
    return True

@app.route("/<path>", methods=["POST"])
def webhook(path: str) -> str:
    if (request.method == "POST"):
        for hook in cfg["webhooks"]:
            if (hook["path"] == request.path):
                if (validate_request(hook, request)):
                    print(1)
                    return ("ok", 200)
    print(0)
    return ("uh oh", 400)

app.run(host=cfg["hostname"], port=cfg["port"], debug=True)