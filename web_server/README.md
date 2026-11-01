# Web server

Ubuntu 16.04 web-server exercises. Each Bash script starts with the required
shebang and an explanatory comment. Service changes use the SysV `service`
command. Installation tasks run as root.

| Task | File | Result |
| --- | --- | --- |
| 0 | `0-transfer_file` | SCP a file into the remote user's home, using the supplied identity and disabling strict host-key checking as required. |
| 1 | `1-install_nginx_web_server` | Install Nginx and serve `Holberton School` at `/` on port 80. |
| 2 | `2-setup_a_domain_name` | Pending the user's registered root domain and public server IP. No fabricated domain is submitted. |
| 3 | `3-redirection` | Install Nginx and return HTTP 301 for `/redirect_me` and `/redirect_me/`. |
| 4 | `4-not_found_page_404` | Install Nginx with the redirect and an error page containing `Ceci n'est pas une page`, preserving HTTP 404. |
| 5 | `404.html`, `5-design_a_beautiful_404_page` | Deploy a responsive, self-contained illustrated 404 page, retaining the required phrase and status. |

Tasks 1, 3, and 4 are standalone scripts: each installs and configures a fresh
Ubuntu machine without sourcing another answer file. Task 5 uses the adjacent
task-4 script and HTML asset. Rerunning these scripts does not duplicate
configuration. The selected script replaces the default Nginx site and home
page; back up customized content before applying it to an existing machine.

## Usage

```sh
./0-transfer_file ./some_page.html SERVER_IP ubuntu ~/.ssh/school
sudo bash ./1-install_nginx_web_server
sudo bash ./3-redirection
sudo bash ./4-not_found_page_404
sudo bash ./5-design_a_beautiful_404_page
```

The SCP usage line is exactly:

```text
Usage: 0-transfer_file PATH_TO_FILE IP USERNAME PATH_TO_SSH_KEY
```

## Domain and external grading

Task 2 needs an actual root domain owned by the student. Its answer file
must contain that domain alone, with a final newline. Configure its root
DNS A record to the assigned web server's public IP and put the domain in
the ALU profile's Project website URL field. The task also asks for the
specified registrar; confirm registration through the course offer.

The local Docker lab uses `172.25.0.11:80`, exposed on the Windows host at
`http://127.0.0.1:8080`. This private address is not a public DNS target.
The ALU sandbox and the assigned web server are separate environments.
External server checks require an assigned, publicly reachable server.

## Public design demo

The `docs` folder publishes the designed page through GitHub Pages. The
task-5 design URL is:

<https://fkangira.github.io/alu-system_engineering-devops/a-little-off-course>

That nonexistent route displays the custom error page with HTTP 404. Its
home links point to the demo's project home. Regenerate the hosted version
after editing `web_server/404.html`:

```sh
python3 web_server/build_pages.py
```

The public design demo does not replace task 2's owned root domain or the
assigned Nginx server required for the server-configuration checks.

After public deployment, the task-5 URL can be a nonexistent path such as
`http://YOUR_DOMAIN/a-little-off-course`, which displays the designed page
while retaining HTTP 404. The HTML uses no external fonts, scripts, images,
or libraries. It supports small screens, keyboard focus, and reduced motion.

## Verification

On Ubuntu with Bash, OpenSSH, and Python 3.5 or newer:

```sh
python3 tests/test_scripts.py -v
shellcheck 0-transfer_file 1-install_nginx_web_server 3-redirection \
  4-not_found_page_404 5-design_a_beautiful_404_page
python3 tests/check_http.py --level 5 --base-url http://127.0.0.1
```

Use level `1`, `3`, `4`, or `5` according to the configuration deployed.
HTTP checks inspect real status codes, content, and redirect headers without
following the external redirect. The unit tests do not modify the machine.

`tests/Dockerfile` builds an Ubuntu 16.04 test client with Python, curl,
OpenSSH, and the distribution's ShellCheck. Nginx is deliberately absent so
installation scripts can be tested on fresh machines.

Reference: Nginx's official documentation for
[error_page](https://nginx.org/en/docs/http/ngx_http_core_module.html#error_page)
and [return](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#return).
