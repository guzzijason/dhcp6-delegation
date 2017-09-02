#!/bin/env python

# http://netaddr.readthedocs.io/en/latest/index.html

import netaddr
from netifaces import interfaces, ifaddresses, AF_INET6
import subprocess
import pprint

addrs = []
prefix = None

for ifaceName in interfaces():
    if ifaceName == 'lo':
      continue
    #addrs = ifaddresses(ifaceName)

    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET6, [{'addr':'No IP addr'}] )]
    pprint.pprint(addresses)
    for a in addresses:
      if a.lower().startswith('fe80:'):
        addresses.remove(a)
      print(a)
    addrs.extend(addresses)

    routes = subprocess.Popen(['/usr/sbin/ip', '-6', 'route', 'list', 'dev', ifaceName, 'proto', 'kernel'], stdout=subprocess.PIPE)
    for line in routes.stdout.readlines():
      p = line.split()[0]
      mylen = netaddr.IPNetwork(p).prefixlen
      if mylen < 64:
        prefix = p

pprint.pprint(addrs)
if len(addrs) == 0:
  raise ValueError('oops!')

#net_compare = len(netaddr.cidr_merge(['2601:43:0:f230:ba27:ebff:fe6e:2ddc','2601:43:0:f230::/62']))
net_compare = len(netaddr.cidr_merge([addrs[0],prefix]))
if net_compare == 1:
  print('in subnet')
