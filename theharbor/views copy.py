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

#def pack_to_ship(request):
#    return render(request, 'pack.html')

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
 
# Logic Below


def test_containers(name):
    name=name.replace("'","")
    cons = c.containers(all=1)
    for each in cons:
        # print name, str(each['Names'])
        if name in str(each['Names']):
           return False
    return True

def build_new_containers(new_containers, arg):
    arg = ()
    for each in new_containers:
        test="c.create_container("+each["image"]+","

        if test_containers(each["name"]):
        # print each["name"], "does not exists"
            for k,v in each.items():
                if "image" not in k:
                    test+=" %s=%s," % ( k, v)

            test=test[:-1]+")"
            #print test
            arg.append(eval(test))
    return arg

def pack_to_ship(request):
    json_data=open('./harbor_master.json')
    data = json.load(json_data)
    json_data.close()

    # pprint(data)

    host1 = data["hosts"][0]["url"]
    # print host1

    c = docker.Client(base_url='http://'+host1,version='1.10',timeout=10)

    new_containers = data["projects"][0]["containers"]
    output = build_new_containers(new_containers)

    returned_data = {'host1':host1, 'new_containers': new_containers, 'output':output}
    return render(request, 'pack.html', returned_data)





