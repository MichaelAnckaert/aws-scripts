import boto3


client = boto3.client("ce")
response = client.get_cost_and_usage(
    TimePeriod={"Start": "2021-06-01", "End": "2021-06-30"},
    Granularity="DAILY",
    Metrics=["UnblendedCost"],
    GroupBy=[
        {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
        {"Type": "DIMENSION", "Key": "SERVICE"},
    ],
)

for item in response["ResultsByTime"][0]["Groups"]:
    service = item["Keys"][1]
    cost_amount = item["Metrics"]["UnblendedCost"]["Amount"]
    cost_amount = float(cost_amount)
    if cost_amount > 0:
        # print(f"{service}: $ {cost_amount}")
        pass
