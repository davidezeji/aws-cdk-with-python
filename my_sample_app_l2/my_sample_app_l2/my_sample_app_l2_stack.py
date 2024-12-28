from constructs import Construct
from aws_cdk import (
   Stack,
   aws_ec2 as ec2 
)


class MySampleAppL2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # this l2 construct creates a VPC with no NAT gateways. Therefore it creates a VPC, 2 public subnets, 2 private (isolated) subnets, IGW, VPC gateway and default security group.
        my_vpc = ec2.Vpc(self, 'MyVpc', 
                         nat_gateways=0)
