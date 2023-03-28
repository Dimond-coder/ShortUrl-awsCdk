from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
)
from constructs import Construct


class ShorterUrlPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Create DynamoDB
        dynamodbTable = dynamodb.Table(self, "mapping-table",
                               partition_key=dynamodb.Attribute(
                                    name="id",
                                    type=dynamodb.AttributeType.STRING))

        #Create Lambda Function
        lamdbaFunction = lambda_.Function(self, "backend",
                                          runtime=lambda_.Runtime.PYTHON_3_9,
                                          handler="handler.main",
                                          code=lambda_.Code.from_asset("./lambda"))
        
        #Add permission to Lambda function
        dynamodbTable.grant_read_write_data(lamdbaFunction)
        #Add Env to lambda function
        lamdbaFunction.add_environment("TABLE_NAME", dynamodbTable.table_name)

        #APT Gateway
        api= apigw.LambdaRestApi(self, "api", handler=lamdbaFunction)