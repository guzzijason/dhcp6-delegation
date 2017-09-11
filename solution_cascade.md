---
title: Enabling cascading of sub-prefixes
layout: page
comments: true
search: true
sidebar: home_sidebar
topnav: topnav
---

## IPv6 eliminates the need for DHCP... except for when you need DHCP

Hosts on IPv6 networks should have no problems autoconfiguring themselves with SLAAC; however, to perform prefix delegation, it is necessary to use DHCP6 as noted on the previous page. When you request a delegated prefix from your ISP, it's done with a DHCP request. Likewise, if you want to be able to delegate sub-prefixes downward in your network tree, you also need to have a DHCP6 server configured to do so.

A DD-WRT router might be able to be coaxed into performing this job, but I'm not sure. I've not personally had much luck getting `dhcpd6`  runinng on DD-WRT, and I haven't tried configuring `dnsmasq` to do so (assuming it can?). The truth is, I haven't had much of need to do this on the DD-WRT router on my network, because in my case, it is the delegation **client**, and nto the delegation **server**. Rather, my DD-WRT router needs to be the one making the delegation request upstream.

So, in a perfect world, the FortiGate in my network would have it's DHCP6 server configured to serve `IA_PD` requests. Currently, that does not seem to be the case. So I had to come up with an alternate solution.

## Set up your own DHCP6 prefix server

As an experiment, I set up a VM on my lab network to act as a DHCP6 server, and then I configured a DHCP relay on the FortiGate to take reuqests from VLAN2, and forward them to the DHCP6 server on VLAN1. I hard-coded the server config based on the delegated prefix I had from my ISP at that time, just to see if it would work. Much to my astonishment, it did... sort of. There was still one roadblock additional problem I had to contend with (I'll get to that in a bit), but the important thing is, my DD-WRT router was receiving a sub-prefix, and successfully adding it to its downstream interface, **AND** hosts on that LAN were successfully autoconfiguring with SLAAC. _"Excelsior!"_

Now that I had a proof-of-concept working, I wanted to make it a little more permanent, as the VMs in my lab environment aren't really intended to be long-term stable - its just a sandbox to play in. So, I decided to buy a Raspberry Pi and set it up as a DHCP server appliance. Specifically, I got a [Rasberry Pi 3 B](https://www.amazon.com/gp/product/B00L87YMGM/) kit, and also a [serial console cable](https://www.amazon.com/gp/product/B00DJUHGHI/) so that I could run it headless. In hindsight, the quad-core Pi 3 B may have been a bit overkill... it's a pretty bad-ass little computer! But the whole kit, with console cable only set me back ~$75, so whatever. I should have bought 10 of them, maybe. But I digress...

With the Pi in-hand, I set about to getting it running, which was remakably easy. I decided to try the [CentOS 7 distribution for the Pi(https://wiki.centos.org/SpecialInterestGroup/AltArch/Arm32/RaspberryPi3), partly because I'm already intimately famliar with CentOS, and also because I knew for a fact that the ISC DHCP server package in CentOS will do exactly what I need. The only complication what figuring out how to get the serial console working, which actually ended up being pretty simple. All you need to do is edit `/boot/config.txt` on the Pi's MicroSD card, and append the line `enable_uart=1` at the end of the file.

Once attached to the FortiGate's VLAN2 network, the next step is to install my [dhcp6-prefix-config.py](https://github.com/guzzijason/dhcp6-delegation/blob/master/dhcp6-prefix-config.py) script (with a few dependencies, see the [README](https://github.com/guzzijason/dhcp6-delegation/blob/master/README.md)) configure the variable in the script (default may just work if you are lucky), and then set up a cron job so it runs periodically.

### What the script does

Referring to the example netowrk diagram on [the previous page](no_cascade.html), you can see that the IPv6 network for VLAN2 is `2601:43:0:1001::/64` (because we configured the FortiGate to assign network "1" of it's delegated ::/62 super-prefix to VLAN2). When the DHCP server autoconfigures itself, it will end up with a network address that looks something like `2601:43:0:1001:abcd:abcd:abcd:2ddc/64`. The config script uses this information as the basis for generating the `dhcpd6` server config file.

By default (see the file itself for default variables), the script will see what it's local (public) IPv6 network is, and then use defined "offset" and "range" values to determine what sub-prefixes it should be configuring in the delegation. So, if the offset is `delegation_offset = 1` and and `delegation_range = 2`, that means it will calculate the following:

```
DHCP server's network  = 2601:43:0:1001::/64
first delegated prefix (offset 1) = 2601:43:0:1002::/64
last delegated prefix (range 2) = 2601:43:0:1003::/64
```

Assuming our ISP gave us a ::/62 prefix, this configuration will deplete all four of our sub-prefixes (remember, `2601:43:0:1000::/64` was assigned to VLAN1 on the FortiGate). Potentially, you could have up to 2 downstream routers satisfied with this configuration. If your ISP decides to change your delegation at some point, running this script periodically (i.e. via cron) will ensure that that the change cascades downstream.

The config script will also set up a local address range for any clients that refuse to use SLAAC (not likely), and also DHCP server options, also for those client that don't want to get this from SLAAC (slightly more likely), but the info above the meat of the situation for prefix delegation. Ensure that DHCP6 server is disabled on the FortiGate for VLAN2, and all IA_PD requests for that VLAN will be served by our (_adorable!_) Pi server.

## Be sure to update firewall policies

By default, the gateway firewall may be blocking any IPv6 traffic originating from inside the network. Take a look at your firewall policy and ensure its set up as you need it to be.

## Oh, one more problem...

{% include image.html file="Columbo.png" alt="Columbo never forgets"  max-width="300"  %}

At this point, there should be IPv6 prefixes cascading down, and hosts on the LAN behind the DD-WRT router are getting addresses. The issue now is, how do you route to them? Traffic can flow out (assuming firewall policies are OK!) and response packets can flow back... but the FortiGate doesn't actually know where to route the responses to. Timeouts!

The solution I came up with for this (and there may be more than one solution) was to enable `RIPng` (the version of RIP that supports IPv6) on both the upstream (`vlan2`) interface on the DD-WRT router, and also on the `VLAN2` interface on the FortiGate.

... details coming soon... 




-----

**[Problem 2 - Can't cascade](problem_cascade.html)<- Previous Page**

-----