# SSH

Ubuntu 20.04 SSH exercises.

| File | Purpose |
| --- | --- |
| `0-use_a_private_key` | Connect as `ubuntu` with `~/.ssh/school`, using only the single-character SSH flags `-i` and `-p`. |
| `1-create_ssh_key_pair` | Generate a 4096-bit RSA key named `school`, protected by the required exercise passphrase `betty`. |
| `2-ssh_config` | Use `~/.ssh/school` for public-key authentication and refuse password and keyboard-interactive authentication. |
| `3-add_authorized_key` | Validate and install a supplied RSA public key for `ubuntu`, preserving existing keys and avoiding duplicate key material. |
| `alu_authorized_key.pub` | The exact ALU task-3 public key supplied for grader access. This is a public key, not a private credential. |

## Generate the key

Run the key-generation script in the directory where you want `school` and
`school.pub` created. For example, from this repository on the ALU sandbox:

```sh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cd ~/.ssh
/alu-system_engineering-devops/ssh/1-create_ssh_key_pair
chmod 600 school
cat school.pub
```

Register the **public** key in your ALU intranet profile. Keep the private
`school` file out of Git. Do not overwrite an existing key pair.

## Connect to the assigned server

```sh
./0-use_a_private_key YOUR_SERVER_IP
```

Without an argument, the script connects to the local Docker lab's `web-01`
at `172.25.0.11:22`, reachable from the lab network. From a Bash environment
on the Windows host, use `./0-use_a_private_key 127.0.0.1 2211` instead.
The other local servers are `web-02` (`172.25.0.12`, host SSH port `2212`)
and `lb-01` (`172.25.0.10`, host SSH port `2210`).

The key must already be authorized for the target server's `ubuntu` user.
A key passphrase prompt is distinct from a remote login password.
The intranet lists a separate assigned server, `7204-web-01`; use its IP
as the first argument when testing that server.

Merge the settings from `2-ssh_config` into `~/.ssh/config`, preserving any
existing host entries. Specific host settings should precede the wildcard
block. Protect the config with `chmod 600 ~/.ssh/config`.

## Task 3: ALU access

This is a change on the assigned server, rather than a repository script.
Add the exact public key shown in task 3 as one line in
`/home/ubuntu/.ssh/authorized_keys`, retaining all existing keys. Ensure the
directory and file belong to `ubuntu`, with modes `700` and `600`
respectively. The ALU sandbox and the assigned server are separate machines.

ALU's exact task-3 key is saved as a single line in `alu_authorized_key.pub`.
From this directory, run this on the target server as `ubuntu` or root:

```sh
bash 3-add_authorized_key alu_authorized_key.pub
```

The installer rejects malformed keys, retains existing entries, and sets
the required permissions. Installing your own `school.pub` does not complete
task 3; ALU's supplied key is required.

The supplied ALU key has RSA size 2048 and fingerprint
`SHA256:83vIEn8QchURHEMBnrJZtEnEHk+Tcb+RB21pzZ4mlRU`.
It has been installed on the local Docker lab's `web-01`, preserving the
existing keys. Reapply it if that container is recreated from its image.

## Verify

From the repository root on Ubuntu:

```sh
python3 test_ssh.py -v
shellcheck ssh/0-use_a_private_key ssh/1-create_ssh_key_pair ssh/3-add_authorized_key
```

The tests check shell syntax, the SSH arguments with a mock client, parsed
client configuration, real RSA key size, the required passphrase, and the
generated public/private key match. They create disposable keys in temporary
directories. They do not connect to the assigned server or install keys.
