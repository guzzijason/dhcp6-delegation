---
title: Example configs for prefix hint requests
layout: page
comments: true
search: true
sidebar: home_sidebar
topnav: topnav
---

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#fortigate" data-toggle="tab">FortiGate</a></li>
    <li><a href="#dd-wrt" data-toggle="tab">DD-WRT</a></li>
</ul>
  <div class="tab-content">
    <div role="tabpanel" class="tab-pane active" id="fortigate">

        <p>
				<pre>
config system interface
    edit "wan"
        config ipv6
            set ip6-mode dhcp
            set ip6-allowaccess ping
            set dhcp6-prefix-delegation enable
            set dhcp6-prefix-hint ::/62
        end
    next
end </pre>
							<pre>
config system interface
    edit "vlan1"
        config ipv6
            set ip6-mode delegated
            set ip6-allowaccess ping
            set ip6-send-adv enable
            set ip6-manage-flag enable
            set ip6-upstream-interface "wan"
            set ip6-subnet 0:0:0:0::/64
            config ip6-delegated-prefix-list
                edit 1
                    set upstream-interface "wan"
                    set autonomous-flag enable
                    set onlink-flag enable
                    set subnet 0:0:0:0::/64
                next
            end
        end
    next
end</pre>
							<pre>
config system interface
    edit "wan"
        config ipv6
            set ip6-mode dhcp
            set ip6-allowaccess ping
            set dhcp6-prefix-delegation enable
            set dhcp6-prefix-hint ::/62
        end
    next
end </pre>
			</p>
      </div>

      <div role="tabpanel" class="tab-pane" id="dd-wrt">

        <p><pre>
Lorem ipsum ...
	    	</pre></p>
      </div>

</div>

-----

** [Problem 1- Prefix too big](prefix64.html) <- Previous Page \| Next Page -> [Problem 2 - Can't cascade](problem_cascade.html)**

-----