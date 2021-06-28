import boto3
import argparse
import csv
import sys


def date_output(v):
    return v.strftime("%d-%m-%Y %H:%m:%s")


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


def get_instances(next_token=""):
    instances = []
    client = boto3.client("ec2")
    response = client.describe_instances(NextToken=next_token)
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append([f[1](instance.get(f[0])) for f in INSTANCE_COLUMNS])

    if response.get("NextToken"):
        instances.extend(get_instances(next_token=response["NextToken"]))

    return instances


def write_csv(instances):
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow([f[0] for f in INSTANCE_COLUMNS])
        for instance in instances:
            writer.writerow(instance)


if __name__ == "__main__":
    print("Retrieving EC2 instances...")
    instances = get_instances()
    print("Writing CSV file")
    write_csv(instances)
    print("Finished!")
