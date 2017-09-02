#!/bin/env python

# http://netaddr.readthedocs.io/en/latest/index.html

import netaddr
from netifaces import interfaces, ifaddresses, AF_INET6
import subprocess

addr_list = []
prefix_list = []
route_list = []

class PrefixException(Exception):
    def __init___(self,msg,prefixes):
      Exception.__init__(self,msg,prefixes)

for ifaceName in interfaces():
    if ifaceName == 'lo':
      continue

    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET6, [{'addr':'No IP addr'}] )]
    for a in addresses:
      if a.lower().startswith('fe80:'):
        addresses.remove(a)
    addr_list.extend(addresses)

    routes = subprocess.Popen(
      ['/usr/sbin/ip', '-6', 'route', 'list', 'dev', ifaceName, 'proto', 'kernel'],
      stdout=subprocess.PIPE)
    for line in routes.stdout.readlines():
      p = line.split()[0]
      mylen = netaddr.IPNetwork(p).prefixlen
      if mylen < 64:
        route_list.append(p)

for p in route_list:
  for a in addr_list:
    if len(netaddr.cidr_merge([a,p])) == 1:
      prefix_list.append(p)
    else:
      prefix_list.remove(p)

if len(prefix_list) == 0:
  raise PrefixException("No adequate prefixes found: size must be <= /63", None)
elif len(prefix_list) > 1:
  raise PrefixException("Too many prefixes - unsure how to proceed", prefix_list)

