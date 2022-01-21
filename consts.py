import boto3

S3 = boto3.client("s3")

NISSAN_MAPPING = {
    "RV": "01",
    "TP": "05",
    "MP": "06",
    "NI": "18",
    "MN": "19",
    "N4": "22",
    "73": "73",
    "GD": "A0",
    "PM": "A4",
    "RB": "AK",
    "CP": "AZ",
}
