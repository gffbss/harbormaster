from django.shortcuts import render, redirect
import docker
import requests
import logging
import json
from random import randint

logging.basicConfig(filename='testing_logs.log', level=logging.INFO)

def index(request):
    return render(request, 'index.html')

def url_c():
    c = docker.Client(base_url='http://dh1.ucount.com:2375', version='1.10', timeout=10)    
    return c

def get_json_data(request):
    q = requests.get('http://dh1.ucount.com:2375/containers/json?all=1')
    containers = q.json()
    data = {'containers': containers}
    return render(request, 'data.html', data)


def prep_docker(request):
    # Get the user inputed container name
    name = request.POST['instance_name']

    c = url_c()
    create = c.create_container('gmaxwell94/ssh_etcd', command='/usr/bin/supervisord', hostname='{}.prod'.format(name), detach=True, stdin_open=True, tty=True, mem_limit=0, ports="[22,8098,8087]", environment=None, dns=None, volumes=None, volumes_from=None, network_disabled=False, name='{}'.format(name), entrypoint=None, cpu_shares=None, working_dir=None)    
    
    parts = json.dumps(create) 
    get_id = json.loads(parts)   
    container_id = get_id['Id']
    data = {'container_id': container_id}  
    return render(request, 'start.html', data)

# Start up the docker instance
def start_docker(request):
    # Get the user inputed container name
    my_con = request.POST.get('instance_id', False)
    logging.info('Check it out:')
    logging.info(my_con)
    # my_con = '88c116c7358afb217bf691ab60d846e491fdb5c1e2f5c6c2fee5ef1d5da31a56'
    rad= randint(100, 999)

    ssh=46000+rad
    http1=46001+rad
    http2=46002+rad

    c = url_c()
    test = c.start(my_con, binds=None, port_bindings={22:ssh,8098:http1,8087:http2}, lxc_conf='docker', publish_all_ports=False, links=None, privileged=False)
    
    #parts = json.dumps(test)    
    #stuff = {'parts': parts}    
    
    #data = {'my_con': my_con}
    return redirect('/data/')
    #return render(request, 'data.html', data)
 

def test_containers(name):
    c = url_c()
    name=name.replace("'","")
    cons = c.containers(all=1)
    for each in cons:
        # print name, str(each['Names'])
        if name in str(each['Names']):
           return False
    return True

def build_new_containers(new_containers):
    c = url_c()
    arg = []
    for each in new_containers:
        test="c.create_container("+each["image"]+","

        if test_containers(each["name"]):
        # print each["name"], "does not exists"
            for k,v in each.items():
                if "image" not in k:
                    test+=" %s=%s," % ( k, v)

            test=test[:-1]+")"
            arg.append(eval(test))
    return arg

# Pack up the container with the name data from user
def pack_to_ship(request):
    json_data=open('./harbor_master.json')
    data = json.load(json_data)
    json_data.close()

    host1 = data["hosts"][0]["url"]

    c = url_c()

    new_containers = data["projects"][0]["containers"]
    output = build_new_containers(new_containers)

    returned_data = {'host1':host1, 'new_containers': new_containers, 'output':output}
    

    # get url params
    #n = request.GET
    #instance_name = n.__getitem__('instance_name')

    return render(request, 'pack.html', returned_data)

#def stop(request):
#    c.stop(id)
#    return render(request, 'pack.html')


