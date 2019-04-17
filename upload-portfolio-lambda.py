import json
import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:794138155809:deployPortfolioTopic')

    try:
        
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        
        portfolio_bucket = s3.Bucket('portfolio.ianbunn.studio')
        build_bucket = s3.Bucket('portfoliobuild.ianbunn.studio')
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.ianbunn.studio', portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        print ("Portfolio has been deployed!")
        topic.publish(Subject="Portfolio deployment completed", Message="https://portfolio.ianbunn.studio")
    except:
        topic.publish(Subject="Portfolio deployment FAILED", Message="The portfolio deployment failed. Please review now and try again.")

    return 'Hello from Lambda'