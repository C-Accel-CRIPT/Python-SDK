"""
# AWS S3 Cognito Config Constants

This file contains the configuration constants for AWS S3,
for when `cript.API` goes to upload/download files from AWS S3 Cognito
"""

_REGION_NAME: str = "us-east-1"
_IDENTITY_POOL_ID: str = "us-east-1:9426df38-994a-4191-86ce-3cb0ce8ac84d"
_COGNITO_LOGIN_PROVIDER: str = "cognito-idp.us-east-1.amazonaws.com/us-east-1_SZGBXPl2j"
_BUCKET_NAME: str = "cript-user-data"

# specific directory for python sdk files
_BUCKET_DIRECTORY_NAME: str = "python_sdk_files"
