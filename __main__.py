import os, hashlib, random, struct

from bottle import get, post, redirect, request, run, static_file
from Crypto.Cipher import AES
        
@get('/')
def encrypt_get():
    return static_file('encrypt.html', root='templates')

@post('/')
def encrypt_post():
    name = request.forms.get('name')
    secret_text = request.forms.get('secrettext')
    
    while(len(secret_text) % 16 != 0):
        secret_text += "|" # Padding

    password = request.forms.get('password').encode("utf-8")

    key = hashlib.sha256(password).digest()

    obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    ciphertext = obj.encrypt(secret_text.encode("utf-8"))
    
    with open("encrypted/{}.txt".format(name), "wb") as f:
        f.write(ciphertext) 

    redirect("/decrypt")

@get('/decrypt')
def decrypt_get():
    return static_file('decrypt.html', root='templates')

@post('/decrypt')
def decrypt_post():
    name = request.forms.get('name')
    password = request.forms.get('password').encode("utf-8")

    key = hashlib.sha256(password).digest()
    obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')

    with open("encrypted/{}.txt".format(name), "rb") as f:
        ciphertext = f.read()
        secret_text = obj.decrypt(ciphertext).decode("utf-8").rstrip("|") # Also remove padding

    return secret_text


if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
