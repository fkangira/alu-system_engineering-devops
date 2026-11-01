#!/usr/bin/python3
"""Check script contracts without installing packages or changing Nginx."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ["0-transfer_file", "1-install_nginx_web_server", "3-redirection",
           "4-not_found_page_404", "5-design_a_beautiful_404_page"]


class ScriptTests(unittest.TestCase):
    """Validate required headers, syntax, and SCP behavior."""

    def test_script_format_and_syntax(self):
        """Every Bash answer is executable and uses the required headers."""
        for filename in SCRIPTS:
            path = ROOT / filename
            source = path.read_bytes()
            self.assertTrue(source.startswith(b"#!/usr/bin/env bash\n#"))
            self.assertTrue(source.endswith(b"\n"))
            self.assertNotIn(b"\r", source)
            self.assertNotIn(b"systemctl", source)
            self.assertTrue(os.access(str(path), os.X_OK))
            subprocess.run(["bash", "-n", str(path)], check=True)

    def test_usage(self):
        """Print the exact required usage for fewer than four arguments."""
        for count in range(4):
            result = subprocess.run(
                ["bash", str(ROOT / "0-transfer_file")] + ["x"] * count,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
            self.assertEqual(result.stdout,
                             "Usage: 0-transfer_file PATH_TO_FILE IP "
                             "USERNAME PATH_TO_SSH_KEY\n")
            self.assertNotEqual(result.returncode, 0)

    def test_scp_arguments_and_exit_status(self):
        """Preserve spaced filenames, disable host checking, and pass errors."""
        with tempfile.TemporaryDirectory() as temp:
            mock = Path(temp) / "scp"
            mock.write_text('#!/bin/sh\nprintf "%s\\0" "$@"\n'
                            'exit "${MOCK_SCP_STATUS:-0}"\n')
            mock.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = temp + os.pathsep + environment["PATH"]
            for status in (0, 7):
                environment["MOCK_SCP_STATUS"] = str(status)
                result = subprocess.run(
                    ["bash", str(ROOT / "0-transfer_file"), "my page.html",
                     "203.0.113.5", "ubuntu", "/keys/my private key"],
                    env=environment, stdout=subprocess.PIPE)
                self.assertEqual(result.returncode, status)
                self.assertEqual(result.stdout.split(b"\0")[:-1], [
                    b"-o", b"StrictHostKeyChecking=no", b"-i",
                    b"/keys/my private key", b"my page.html",
                    b"ubuntu@203.0.113.5:~/"])


if __name__ == "__main__":
    unittest.main()
