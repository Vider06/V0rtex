import socket
import requests

def fake_eval_demo(code):
    return eval(code)

def fake_exec_demo():
    exec("print('hello from exec')")

def network_probe():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def http_call():
    return requests.get("https://example.com")

def crypto_like():
    data = "test"
    return hash(data)

if __name__ == "__main__":
    fake_eval_demo("2 + 2")
    fake_exec_demo()
    network_probe()
    http_call()
    crypto_like()