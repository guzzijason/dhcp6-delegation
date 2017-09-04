#!/bin/env python

from filecmp import cmp
from jinja2 import Template
from netifaces import interfaces, ifaddresses, AF_INET6
from shutil import copyfile
from tempfile import mkstemp
import datetime, netaddr, os, subprocess, sys
import logging, logging.handlers


### start configurables

conf_file = '/etc/dhcp/dhcpd6.conf'
default_lease_time = '604800'        # dhcp6 vltime
preferred_lifetime = '345600'        # dhcp6 pltime

### end configurables


myname = os.path.basename(__file__)
myaddr_list = []    # my IPv6 interface addrs
myprefix_list = []  # my /64 prefixes from local interfaces
route_list = []     # IPv6 routes advertised from our gw
prefix_list = []    # upstream prefixes avaialbe for sub-delegation


# set up logging
my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)
formatter = logging.Formatter('%(module)s: %(message)s')
handler.setFormatter(formatter)


# loop through interfaces and find advertised IPv6 routes
for ifaceName in interfaces():
    if ifaceName == 'lo':
      # skip loopback
      continue

    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET6, [{'addr':'No IP addr'}] )]

    for a in addresses:
      # discard link-local addrs
      if a.lower().startswith('fe80:'):
        continue
      else:
        myaddr_list.append(a)

    routes = subprocess.Popen(
      ['/usr/sbin/ip', '-6', 'route', 'list', 'dev', ifaceName, 'proto', 'kernel'],
      stdout=subprocess.PIPE)

    for line in routes.stdout.readlines():
      # discard link-local routes
      p = line.split()[0]
      if p.lower().startswith('fe80:'):
        continue
      else:
        route_list.append(p)


# for each advertised route, determine if it's our local subnet
# or not.
for p in route_list:
  for a in myaddr_list:
    if len(netaddr.cidr_merge([a,p])) == 1:   # true if this is our subnet
      if netaddr.IPNetwork(p).prefixlen < 64: # true if upstream super-prefix
        prefix_list.append(p)
      else:                                   # my local prefix
        myprefix_list.append(p)
    else:                                     # foreign subnets
      if netaddr.IPNetwork(p).prefixlen < 64: # not available for delegation
        prefix_list.remove(p)
      else:                                   # do not configure as local
        myprefix_list.remove(p)


# hopefully, we found 1 upstream prefix that matches our criteria for breaking
# into sub-prefix(es) for delegation. More or less than 1 is a problem
if len(prefix_list) == 0:
  my_logger.error('No adequate prefixes found: size must be <= /63')
  sys.exit(1)
elif len(prefix_list) > 1:
  my_logger.error('Too many prefixes - unsure how to proceed')
  my_logger.error('Found prefixes %s' % prefix_list)
  sys.exit(1)


# calculate our list of potential /64 sub-prefixes based on discovered prefix
ip = netaddr.IPNetwork(prefix_list[0])
delegations = list(ip.subnet(64))


# define our DHCP server config template
config = Template('''# generated by {{ script }}
#
default-lease-time {{ ldefault }};
preferred-lifetime {{ lpreferred }};
log-facility local7;
option dhcp6.name-servers 2001:558:FEED::1,2001:558:FEED::2;
subnet6 {{ subnet6 }} {
       # Range for clients
       range6 {{ range_start }} {{ range_end }};
       # Prefix range for delegation to sub-routers
       prefix6 {{ prefix_start }} {{ prefix_end }} /64;
}

''')


# open temp file, write config
fd, temp_file = mkstemp(prefix="dhcp6s.")
os.write(fd, config.render(
  ldefault=default_lease_time,
  lpreferred=preferred_lifetime,
  script=myname,
  range_start=netaddr.IPNetwork(prefix_list[0])[101],
  range_end=netaddr.IPNetwork(prefix_list[0])[200],
  prefix_start=delegations[1].ip,
  prefix_end=delegations[2].ip,
  subnet6=myprefix_list[0]
  )
)
os.close(fd)


# if new config differs from running config, install and restart server
if cmp(temp_file, conf_file):
  test = "foobar"
  my_logger.info('dhcpd6 configuration unchanged')
else:
  print("updating", conf_file)
  copyfile(temp_file, conf_file)
  os.remove(temp_file)
  my_logger.info('dhcpd6 configuration updated')
  subprocess.call(['systemctl', 'restart', 'dhcpd6'])
