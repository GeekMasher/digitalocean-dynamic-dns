#!/usr/bin/env python
import os
import requests
import argparse

parser = argparse.ArgumentParser(description="Dynamic DNS for Digital Ocean")
parser.add_argument(
    "-d", "--domain", default=os.environ.get("DOMAIN"), help="Domain name to update"
)
parser.add_argument(
    "--token", help="Digital Ocean API Token", default=os.environ.get("DO_AUTH_TOKEN")
)
parser.add_argument(
    "-n", "--name", default=os.environ.get("DOMAIN_NAME"), help="Record name"
)
parser.add_argument("-t", "--type", default="A", help="Record type")
parser.add_argument("-i", "--ip", help="IP address to update")


def getExternalIP():
    r = requests.get("http://checkip.amazonaws.com")
    return r.text.strip()


def getDNSRecord(token, domain, record_name, record_type):
    url = "https://api.digitalocean.com/v2/domains/{}/records".format(domain)
    headers = {"Authorization": "Bearer {}".format(token)}
    data = {"type": record_type, "name": record_name}
    r = requests.get(url, headers=headers, data=data)

    data = r.json()

    # get record by name
    for record in data.get("domain_records"):
        if record["name"] == record_name and record["type"] == record_type:
            return record
    return {}


def updateDNSRecord(token, domain, record, ip):
    url = "https://api.digitalocean.com/v2/domains/{}/records/{}".format(
        domain, record.get("id")
    )
    headers = {"Authorization": "Bearer {}".format(token)}
    data = {"type": record["type"], "name": record["name"], "data": ip}
    r = requests.put(url, headers=headers, data=data)

    data = r.json()

    return data


if __name__ == "__main__":
    args = parser.parse_args()

    if not args.token:
        print("Please provide a token")
        exit(1)
    if not args.domain:
        print("Please provide a domain")
        exit(1)
    if not args.name:
        print("Please provide a name")
        exit(1)

    ip = args.ip or getExternalIP()

    print(f"External IP Address :: {ip}")

    record = getDNSRecord(args.token, args.domain, args.name, args.type)

    if record:
        print(f"Record already exists :: {record}")
        if record["data"] == ip:
            print("IP address already set")
            exit(0)
        else:
            print(f"Updating record :: {record}")
            data = updateDNSRecord(args.token, args.domain, record, ip)
            print(f"Record updated :: {data}")
