import boto3


def upload_file(fn):
    """Upload file to AWS S3
    
    Arguments:
        fn {string} -- Filename
    """

    s3 = boto3.client(
        "s3",
        aws_access_key_id=config["s3-access-key"],
        aws_secret_access_key=config["s3-secret-access-key"],
    )

    s3.upload_file(Bucket=config["s3-bucket"], Filename=fn, Key=fn)

    return f"https://{bucket}.s3.eu-west-2.amazonaws.com/{fn}"
