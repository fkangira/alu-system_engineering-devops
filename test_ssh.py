#!/usr/bin/python3
"""Verify the SSH exercises on Ubuntu without touching existing keys."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent / "ssh"


class SshTests(unittest.TestCase):
    """Validate script behavior and real OpenSSH key generation."""

    def test_script_headers_and_syntax(self):
        """Both scripts have required headers and valid Bash syntax."""
        for name in ("0-use_a_private_key", "1-create_ssh_key_pair"):
            script = ROOT / name
            source = script.read_bytes()
            self.assertTrue(source.startswith(b"#!/usr/bin/env bash\n#"))
            self.assertTrue(source.endswith(b"\n"))
            self.assertNotIn(b"\r", source)
            self.assertTrue(os.access(str(script), os.X_OK))
            subprocess.run(["bash", "-n", str(script)], check=True)

    def test_connection_arguments(self):
        """Use the school key, ubuntu user, and only a permitted short flag."""
        with tempfile.TemporaryDirectory() as temp:
            mock = Path(temp) / "ssh"
            mock.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
            mock.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = temp + os.pathsep + environment["PATH"]
            for host in ("203.0.113.10", "172.25.0.11", "127.0.0.1"):
                arguments = [] if host == "172.25.0.11" else [host]
                port = "2211" if host == "127.0.0.1" else "22"
                if host == "127.0.0.1":
                    arguments.append(port)
                result = subprocess.run(
                    ["bash", str(ROOT / "0-use_a_private_key")] + arguments,
                    env=environment, check=True, stdout=subprocess.PIPE,
                    universal_newlines=True)
                self.assertEqual(result.stdout.splitlines(), [
                    "-i", os.path.expanduser("~/.ssh/school"), "-p", port,
                    "ubuntu@" + host])

    def test_client_configuration(self):
        """OpenSSH resolves the required identity and forbids passwords."""
        result = subprocess.run(
            ["ssh", "-G", "-F", str(ROOT / "2-ssh_config"),
             "ubuntu@203.0.113.10"], check=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        options = {}
        for line in result.stdout.splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                options[parts[0]] = parts[1]
        self.assertEqual(options.get("user"), "ubuntu")
        self.assertEqual(options.get("identityfile"), "~/.ssh/school")
        self.assertEqual(options.get("passwordauthentication"), "no")
        self.assertEqual(options.get("kbdinteractiveauthentication"), "no")
        self.assertEqual(options.get("preferredauthentications"), "publickey")

    def test_actual_key_generation(self):
        """Generate the required RSA key, confirm size, encryption and match."""
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(
                ["bash", str(ROOT / "1-create_ssh_key_pair")], cwd=temp,
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            private_key = Path(temp) / "school"
            public_key = Path(temp) / "school.pub"
            self.assertTrue(private_key.is_file())
            self.assertTrue(public_key.is_file())
            public_parts = public_key.read_text().split()
            self.assertEqual(public_parts[0], "ssh-rsa")
            info = subprocess.run(
                ["ssh-keygen", "-l", "-f", str(public_key)], check=True,
                stdout=subprocess.PIPE, universal_newlines=True)
            self.assertEqual(info.stdout.split()[0], "4096")
            derived = subprocess.run(
                ["ssh-keygen", "-y", "-P", "betty", "-f", str(private_key)],
                check=True, stdout=subprocess.PIPE, universal_newlines=True)
            self.assertEqual(derived.stdout.split()[:2], public_parts[:2])
            wrong_passphrase = subprocess.run(
                ["ssh-keygen", "-y", "-P", "", "-f", str(private_key)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertNotEqual(wrong_passphrase.returncode, 0)


if __name__ == "__main__":
    if not all(shutil.which(command) for command in ("bash", "ssh-keygen")):
        raise SystemExit("Run these tests on Ubuntu with Bash and OpenSSH.")
    unittest.main()
