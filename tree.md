---
title: Example Tree Network
layout: page
comments: true
search: true
sidebar: home_sidebar
topnav: topnav
---

## Diagram

![](images/Network_Overview.png)

## Description

This example is more similar to what I'm dealing with in my home. In this particular example, the switch on the main edge gateway has been split into multiple port-based <a href="#" data-toggle="tooltip" data-original-title="{{site.data.glossary.VLAN}}">VLANs</a>, which in this case are "VLAN1" and "VLAN2".

**VLAN1** is not doing anything terribly fancy - there is simply another switch that hosts are connected to, it one single broadcast domain. This means that (FortiGate) gateway is **THE** gateway for any devices connected to VLAN1, and the FortiGate can provide addressing to VLAN1 clients via DHCP, SLAAC, static configs, etc. For all intents and purposes, VLAN1 is identical to the fan type network described on the [previous page](fan.html).

**VLAN2** is where things start getting more interesting. On this VLAN, there is a second router ([DD-WRT] in this case) providing service to both Wi-Fi and wired clients on a completely separate network. Clients behind the DD-WRT router get their addressing from DD-WRT, and use that router as their gateway. The DD-WRT router, in turn, uses the FortiGate as it's gateway to the rest of the network, and the Internet. The FortiGate can't "see" hosts that are behind the DD-WRT; it only knows how to  get to them by way of the other router.

This still isn't a terribly complex, but the fact that we now have a routed branch in our network, it's basically considered a "tree" network, rather than a simple "fan". And now that we have an understanding of this sort of network, lets talk about where things can potentially go off the rails in the IPv6 network...

-----

**[Example Fan Network](fan.html) <- Previous Page \| Next Page -> [Problem 1 - Prefix too big](prefix64.html)**


[DD-WRT]: http://www.dd-wrt.com/site/index