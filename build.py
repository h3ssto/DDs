#!/usr/bin/env python3

import re
from jinja2 import Template

from licenses import licenses

def lookup_license(license):

    if license:
        out = {"name": license}
    else:
        out = {"name": "N/A"}

    if license in licenses:
        out["url"] = licenses[license]

    return out

def main():        
    with open("libraries.csv") as file:
        lines = file.readlines()

    entries = []

    for line in lines[2:]:
        entry = {}

        fields = re.split(";", line)

        entry["name"] = fields[0]
        entry["license"] = lookup_license(fields[1])

        entry["last_updated"] = fields[2]

        langs = fields[3]
        langs = re.split(",", langs)
        entry["langs"] = langs

        url = fields[4]
        entry["url"] = {"url": url}
        if "github.com" in url:
            entry["url"]["github"] = True

        entry["users"] = []

        users = re.split(",", fields[5])

        for x in users:
            x = re.split("::", x)

            if len(x) == 1:
                if "github.com" in x[0]:
                    entry["users"].append({"name": x[0], "url": x[0], "github": True})
                else: 
                    entry["users"].append({"name": x[0]})
            else:
                if "github.com" in x[1]:
                    entry["users"].append({"name": x[0], "url": x[1], "github": True})
                else:
                    entry["users"].append({"name": x[0], "url": x[1]})

        entry["affiliations"] = re.split(",", fields[6])
        entry["interfaces_with"] = []

        if fields[8]:
            entry["interfaces_with"] = re.split("&", fields[8])

        entries.append(entry)

    with open("index.j2") as file:
        template = Template(file.read())

    s = template.render(entries = entries)

    with open("index.html", "w") as file:
        file.write(s)

main()