#!/usr/bin/env python3

import argparse
import csv
import sys
from typing import List

import boto3


def date_output(v):
    return v.strftime("%d-%m-%Y %H:%m:%s")


# A list of colum name, converter pairs. The column name will be extracted from the instance data and passed to the
# converter function.
INSTANCE_COLUMNS = [
    ("InstanceId", str),
    ("InstanceType", str),
    ("KeyName", str),
    ("LaunchTime", date_output),
    ("VpcId", str),
    ("SubnetId", str),
    ("PublicIpAddress", str),
    ("PrivateIpAddress", str),
]


def get_instances(region: str, next_token: str = "") -> List[str]:
    """Get EC2 instances from the AWS API and return a list of instance information"""
    instances = []
    client = boto3.client("ec2", region_name=region)
    response = client.describe_instances(NextToken=next_token)
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append([f[1](instance.get(f[0])) for f in INSTANCE_COLUMNS])

    if response.get("NextToken"):
        instances.extend(get_instances(region, next_token=response["NextToken"]))

    return instances


def write_csv(instances: List[str], filename: str):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow([f[0] for f in INSTANCE_COLUMNS])
        for instance in instances:
            writer.writerow(instance)


def run(filename: str, region: str = None):
    print("Retrieving EC2 instances...")
    instances = get_instances(region)
    print(f"Writing CSV file '{filename}'")
    write_csv(instances, filename)
    print("Finished!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Output EC2 instance information to a CSV file"
    )
    parser.add_argument(
        "-f",
        "--filename",
        default="output.csv",
        metavar="filename",
        type=str,
        help="Filename to write the output to",
    )
    parser.add_argument(
        "--region",
        default=None,
        type=str,
        help="Region to collection instance information in",
    )

    args = parser.parse_args()

    run(region=args.region, filename=args.filename)
