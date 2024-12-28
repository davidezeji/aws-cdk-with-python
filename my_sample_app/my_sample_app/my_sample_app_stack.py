from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class MySampleAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # my_vpc is the name of the resource
        my_vpc = ec2.CfnVPC(self, 'MyVpc', 
                            cidr_blcok='10.0.0.0/16',
                            enable_dns_hostnames=True,
                            enable_dns_support=True)
        
        internet_gateway = ec2.CfnInternetGateway(self, 'InternetGateway')

        #this construct attaches the IGW to the VPC
        ec2.CfnVPC
