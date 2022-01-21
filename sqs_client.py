# import json
# import boto3
# import aws_config as settings
# import os.path
# import os

# SQS = boto3.client("sqs", settings.SQS_REGION_NAME)


# while True:
#     messages: list[dict] = []
#     entries_to_delete: list[list[dict]] = []
#     processed_paths: list[str] = []

#     while True:
#         response: dict = SQS.receive_message(
#             QueueUrl=settings.sqs_queue_url,
#             AttributeNames=[
#                 'SentTimestamp'
#             ],
#             MaxNumberOfMessages=10,
#             MessageAttributeNames=[
#                 'All'
#             ],
#             VisibilityTimeout=5,
#             WaitTimeSeconds=0
#         )

#         messageList: list[dict] = response.get("Messages", [])
#         if not len(messageList):
#             break
#         messages.extend(messageList)

#     messages = sorted(messages, key=lambda x: x["Attributes"]["SentTimestamp"], reverse=True)

#     if not os.path.exists("./script-res"):
#         os.makedirs("./script=res")

#     for message in messages:
#         processed = False

#         if not processed:
#             message_body: dict = json.loads(message["Body"])
#             if "Records" not in message_body.keys():
#                 continue
#             message_body = message_body["Records"][0]
#             # ignore if not ObjectCreated:Put
#             if message_body["eventName"] != "ObjectCreated:Put":
#                 continue
#             # ignore if not the s3 dev bucket
#             if message_body["s3"]["bucket"]["name"] != settings.bucket_name:
#                 continue

#             file_path = message_body["s3"]["object"]["key"]
            
#             # delete output file message
#             if settings.output_folder in file_path:
                

