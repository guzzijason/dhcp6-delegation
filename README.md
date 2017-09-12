# dhcp6-delegation
Script for dynamically generating isc-dhcp-server6 sub-prefix delegation based on an upstream delegation

### For some indepth information regarding the rationale behind these scripts, please read this:
### https://guzzijason.github.io/dhcp6-delegation/


-----

## Scripts

**[dhcp6-prefix-config.py](dhcp6-prefix-config.py)**

A tool for generating dhcpd6 IPv6 prefix sub-delegation configs for the [ISC DHCP] server.  
Tested on **CentOS 7.3.1611**.

**Install:**

1. `yum install dhcp python-netaddr python-jinja2`
2. copy script to server
3. `chmod 755 /path/to/dhcp6-prefix-config.py`
4. `systemctl enable dhcpd6`
4. set up cron job to run **as root** on some periodic basis (in case upstream ISP delegation changes and a new config needs to be generated)

-----

**[ripng_dd-wrt.startup](ripng_dd-wrt.startup)**

Startup script for DD-WRT routers that enables **ripngd** to aid in routing IPv6 subnets (such as those that have been delegated from an ISP) to other routers on your local network.  
Tested on **DD-WRT v3.0-r32170 big (06/01/17)** firmware.

**Install:**

1. enable [JJFS filesystem]
2. place script in `/jffs/etc/config/ripng_dd-wrt.startup`
3. `chmod 755 /jffs/etc/config/ripng_dd-wrt.startup`
4. run script by hand **OR** reboot router to start `ripngd`


[ISC DHCP]: http://isc.org/products/DHCP/
[JJFS filesystem]: https://www.dd-wrt.com/wiki/index.php/JFFS
