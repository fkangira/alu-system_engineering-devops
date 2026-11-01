#!/usr/bin/python3
"""Copy the custom 404 into the public demo with project-relative home links."""

from pathlib import Path


def build():
    """Generate the Pages error document from the Nginx HTML source."""
    root = Path(__file__).resolve().parent
    source = (root / "404.html").read_text(encoding="utf-8")
    project_home = "/alu-system_engineering-devops/"
    output = source.replace('href="/"', 'href="{}"'.format(project_home))
    output = output.replace(
        "location.href = '/';",
        "location.href = '{}';".format(project_home))
    destination = root.parent / "docs"
    destination.mkdir(exist_ok=True)
    (destination / "404.html").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    build()
