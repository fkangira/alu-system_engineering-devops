# Load balancer

Two web servers behind an HAProxy load balancer.

| Task | File | Result |
| --- | --- | --- |
| 0 | `0-custom_http_response_header` | Install Nginx (Holberton School page, `/redirect_me` 301, custom 404) and add the `X-Served-By` header set to the server hostname. |
| 1 | `1-install_load_balancer` | Install HAProxy, send traffic to web-01 (18.133.239.146) and web-02 (35.177.254.240) using roundrobin, manageable through its init script. |

Both scripts configure a brand new Ubuntu machine and run as root.
