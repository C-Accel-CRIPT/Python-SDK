from typing import Any

import boto3
from beartype import beartype


@beartype
def get_s3_client(region_name: str, identity_pool_id: str, cognito_login_provider: str, storage_token: str) -> Any:
    """
    Creates an AWS S3 client and returns it to be used in the `cript.API` class.

    Parameters
    ----------
    region_name: str
        AWS S3 region name
    identity_pool_id: str
        AWS S3 identity pool id
    cognito_login_provider: str
        AWS S3 cognito login provider
    storage_token: str
        AWS S3 storage token gotten from the CRIPT frontend

    Returns
    -------
    boto3.client
        fully working AWS S3 client
    """
    auth = boto3.client("cognito-identity", region_name=region_name)
    identity_id = auth.get_id(IdentityPoolId=identity_pool_id, Logins={cognito_login_provider: storage_token})
    aws_token = storage_token

    aws_credentials = auth.get_credentials_for_identity(IdentityId=identity_id["IdentityId"], Logins={cognito_login_provider: aws_token})
    aws_credentials = aws_credentials["Credentials"]
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["AccessKeyId"],
        aws_secret_access_key=aws_credentials["SecretKey"],
        aws_session_token=aws_credentials["SessionToken"],
    )
    return s3_client
