---
title: Unable to cascade prefix
layout: page
comments: true
search: true
sidebar: home_sidebar
topnav: topnav
---

![](images/No_Cascade.png)

## The next roadblock on the way to site-wide autoconf

Now that we have been delegated an appropriately sized prefix, we need to put it to use. In our example, this is what we have:

```
delegated prefix = 2601:43:0:1000::/62
       network 1 = 2601:43:0:1000::/64  [ allocate to VLAN1 ]
       network 2 = 2601:43:0:1001::/64  [ allocate to VLAN2 ]
       network 3 = 2601:43:0:1002::/64  [ available for sub-delegation ]
       network 4 = 2601:43:0:1003::/64  [ available for sub-delegation ]
```

The quick 'n dirty way to get one of the available sub-prefixes assigned to your routed LAN network would be to manually configure the inside interface (e.g. the "br0" bridge interface on a DD-WRT router) with a static address from one available networks, and ensure that <a href="#" data-toggle="tooltip" data-original-title="{{site.data.glossary.route-advertisements}}">route advertisements</a> are enabled, such as by configuring the [radv daemon](https://en.wikipedia.org/wiki/Radvd) on the router. Unfortunately, the problem with static configurations is that your upstream delegation is dynamic - it may change at the discretion of your ISP. If that happens, your downstream config is busted.

If the CPE gateway device (the FortiGate in this example) can already support cascading sub-prefixes to interior routers, then you may be good to go at this point. I In my situation, however, this wasn't the case. While the FortiGate has _excellent_ support for [RFC 3633 IA_PD delegation] on the _CLIENT_ side,( as of this writing) the DHCP6 _SERVER_ in FortiOS doesn't appear to support it.

I believe DD-WRT has a DHCP6 server which _may_ be able to handle prefix delegation, but I haven't tried it out. If it does, it would also require either static conifiguration, or scripting of some sort of dynamic config. (I'll discuss just such a scripting solution for another linux implimentation later on in this document, but DD-WRT is pretty bare-bones so I don't know how easy it would be to impliment at that level).

In any case, I was stuck. I had the prefixes, but couldn't dynamically apply them. IPv6 was working everywhere except for on the primary LAN used by household clients. All dressed up with no place to go, as it were.

{% include callout.html content="If you have a SOHO-class gateway device that you know natively supports DHCP6 IA_PD delegation, please... let us know about it in the comments! " type="info" %} 

-----

**[Problem 1 - Prefix too big](prefix64.html) <- Previous Page \| Next Page -> [Solution 1 - Prefix hinting](solution_prefix.html)**

-----


[RFC 3633 IA_PD delegation]: https://tools.ietf.org/html/rfc3633#section-10