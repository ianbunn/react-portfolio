import json
import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    
    portfolio_bucket = s3.Bucket('portfolio.ianbunn.studio')
    build_bucket = s3.Bucket('portfoliobuild.ianbunn.studio')
    
    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
    
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for name in myzip.namelist():
            obj = myzip.open(name)
            portfolio_bucket.upload_fileobj(obj, name)
            portfolio_bucket.Object(name).Acl().put(ACL='public-read')
    return 'Hello from Lambda'