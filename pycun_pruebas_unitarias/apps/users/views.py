from django.shortcuts import render


def login(username, password):
    if (username == "uskokrum2010") and (password == "123456"):
        return True
    else:
        return False
