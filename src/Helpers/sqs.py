import boto3
import json
client = boto3.client(
    'sqs',
  
)

queue_url = 

# Functions to deal with SQS queue


def push_message_to_queue(finalJSON):
    response = client.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageBody=(str(finalJSON)),
        MessageGroupId="generalise",
    )
    print(response['MessageId'])


def receive_message_from_queue():
    response_from_sqs = json.loads(json.dumps(
        client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10
        ),
        indent=4)
    )
    print("\nInside Queue Handler\n")
    message_to_be_sent = []
    # print(response_from_sqs["messages"])
    for responses in response_from_sqs.get("Messages", []):
        modified_json = {
            "Body": json.loads(responses["Body"]),
            "ReceiptHandle": responses["ReceiptHandle"]
        }
        message_to_be_sent.append(modified_json)
    return message_to_be_sent


def delete_message_from_queue(receipt_handle):
    print(receipt_handle)
    receipt_handle = receipt_handle
    print(client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    ))