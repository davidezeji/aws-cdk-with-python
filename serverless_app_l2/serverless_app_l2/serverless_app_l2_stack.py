from aws_cdk import (
    RemovalPolicy,
    CfnOutput, # needed to be able to get the output from the command 
    Duration, # Duration is used by cloudwatch to configure periods of time.
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_cloudwatch as cloudwatch # needed to create CloudWatch metrics and alarms.
)
from constructs import Construct

class ServerlessAppL2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a DynamoDB table for storing product information.
        products_table = dynamodb.Table(self, 'ProductsTable', 
                                        partition_key=dynamodb.Attribute(
                                        name='id', 
                                        type=dynamodb.AttributeType.STRING
                                        ),
                                        billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                        removal_policy=RemovalPolicy.DESTROY)
        
        # Create a Lambda function for retrieving product information (retrieves it from the lambda function 'lambda_handler' created in product_list_function.py).
        product_list_function = lambda_.Function(self, 'ProductListFunction', 
                                                runtime=lambda_.Runtime.PYTHON_3_10, 
                                                handler='product_list_function.lambda_handler', 
                                                code=lambda_.Code.from_asset('lambda_src'), # lambda_src is the directory containing the lambda function code. 
                                                environment={
                                                    'TABLE_NAME': products_table.table_name
                                                    })
    
        # Granting permissions to the Lambda function to read data from the DynamoDB table
        products_table.grant_read_data(product_list_function.role) 
        
        # Adding a Lambda URL to the Lambda function to execute it from the Internet.
        product_list_url = product_list_function.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE) 

        # Adding a stack output for the function URL to access it easily
        CfnOutput(self, 'ProductListUrl',
                  value=product_list_url.url)
        
        # Configuring an alarm for the Lambda function's errors metric
        error_metric = product_list_function.metric_errors(
            label='ProductListFunction Errors',
            period=Duration.minutes(5),
            statistic=cloudwatch.Stats.SUM
        )

        error_metric.create_alarm(self, 'ProductListErrorsAlarm',
                                  evaluation_periods=1,
                                  threshold=1,
                                  comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                                  treat_missing_data=cloudwatch.TreatMissingData.IGNORE)

        
        
                                        
