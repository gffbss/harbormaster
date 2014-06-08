from django.shortcuts import render
import requests
import logging

def index(request):
    return render(request, 'index.html')

def get_json_data(request):
    q = requests.get('http://dh1.ucount.com:2375/containers/json?all=1')
    stuff = q.json()
    data = {'stuff': stuff}
    return render(request, 'data.html', data)


