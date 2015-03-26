import os
import sys
import subprocess
import pprint

import yaml
import docker


DEV_NULL = open('/dev/null', 'w')


def setup_consul(config):
    import consul
    c = consul.Consul()
    path = config['path'].strip('/')
    for key, value in config['data'].items():
        key = path + '/' + key
        c.kv.put(key, value, cas=0)


def check_setup():
    # check permissions
    if os.getuid() != 0:
        print 'Must be run as root'
        sys.exit(1)

    # check weave running
    ret = subprocess.call(['weave', 'status'], stdout=DEV_NULL)
    if ret != 0:
        print 'weave is not running'
        sys.exit(1)


def run(ip, name, *args):
    print name,
    cmd = ['weave', 'run', ip, '--name', name]
    cmd.extend(args)
    re = subprocess.call(cmd)
    assert re == 0


def compose():
    check_setup()

    base_path = os.path.abspath(os.curdir)
    data = yaml.load(open(os.path.join(base_path, 'app.yml')))
    pprint.pprint(data)
    config = data.get('_config', {})
    subnet = str(config['subnet'])  # TODO auto
    global_config = data.get('_global', {})
    consul_config = config.get('consul')
    setup_consul(consul_config)

    dock = docker.Client()
    # dock.build()
    # containers = dock.containers(all=True)

    container = [name for name in data if not name.startswith('_')]

    # remove containers
    for name in container:
        name = config['prefix'] + '.' + name
        try:
            dock.remove_container(name, force=True)
        except docker.errors.APIError:
            pass

    # start containers
    global_env = global_config.get('environment', [])
    global_env.append('CONFD_OPT=-node {}:8500 -backend consul'.format(config['self']))

    for name in container:
        container_data = data[name]
        name = config['prefix'] + '.' + name
        print 'start', name
        ip = container_data['ip'] + '/' + subnet  # TODO auto

        cmd = [ip, name]
        # volumes
        host_data_path = base_path + '/'
        for volume in container_data.get('volumes', []):
            print host_data_path + volume
            cmd.extend(['-v', host_data_path + volume])

        # envirument varialbes
        for env in container_data.get('environemnt', []) + global_env:
            cmd.extend(['-e', env])

        cmd.extend(['-d', container_data['image']])
        print cmd

        run(*cmd)

    re = subprocess.call(['weave', 'expose', config['self'] + '/' + subnet])
    assert re == 0, 'expose weave'
