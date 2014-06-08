from django.shortcuts import render
import docker
import requests
import logging
import json

def index(request):
    return render(request, 'index.html')

def get_json_data(request):
    q = requests.get('http://dh1.ucount.com:2375/containers/json?all=1')
    stuff = q.json()
    data = {'stuff': stuff}
    return render(request, 'data.html', data)

def pack_to_ship(request):
    return render(request, 'pack.html')

def start_docker(request):
#    i_name = 'maxwell-10x'
    i_name = 'maxwell-11x'
#    params = requests.get
#    check = 'instance_name'
#    if check in params:
#        instance = params.__getitem__('instance_name')

    c = docker.Client(base_url='http://dh1.ucount.com:2375', version='1.10', timeout=10)
    test = c.create_container('ubuntu:13.10', command='/bin/bash', hostname='dh1-x.ucount.com', detach=True, stdin_open=True, tty=True, mem_limit=0, ports=8001, environment=None, dns=None, volumes=None, volumes_from=None, network_disabled=False, name='{}'.format(i_name), entrypoint=None, cpu_shares=None, working_dir=None)    
    
    parts = json.dumps(test)    
    stuff = {'parts': parts}    
    
    return render(request, 'start.html', stuff)
 
