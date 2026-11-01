#!/usr/bin/python3
"""Verify real HTTP responses from an already configured Nginx server."""

import argparse
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Expose redirect responses without contacting the target website."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        """Keep the original redirect response available to the test."""
        return None


def verify(base_url, level):
    """Check page content, redirect status and custom error responses."""
    opener = urllib.request.build_opener(NoRedirect)

    def fetch(path):
        """Fetch a response including HTTP error bodies."""
        try:
            return opener.open(base_url.rstrip("/") + path, timeout=15)
        except urllib.error.HTTPError as error:
            return error

    with fetch("/") as response:
        assert response.code == 200, "Home page must return HTTP 200"
        assert b"Holberton School" in response.read(), "Missing home text"
    if level >= 3:
        for path in ("/redirect_me", "/redirect_me/"):
            with fetch(path) as response:
                assert response.code == 301, "Redirect must use HTTP 301"
                assert response.headers.get("Location") == (
                    "https://www.youtube.com/watch?v=QH2-TGUlwu4")
    if level >= 4:
        for path in ("/missing-page-for-test", "/another/missing/page"):
            with fetch(path) as response:
                assert response.code == 404, "Missing page must stay HTTP 404"
                body = response.read()
                assert b"Ceci n'est pas une page" in body
                if level >= 5:
                    assert b"<!doctype html>" in body.lower()
                    assert b"A little" in body and b"off course." in body
    print("PASS: real HTTP checks for task {} at {}".format(level, base_url))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1")
    parser.add_argument("--level", type=int, choices=(1, 3, 4, 5), required=True)
    args = parser.parse_args()
    verify(args.base_url, args.level)
