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
                            cidr_block='10.0.0.0/16',
                            enable_dns_hostnames=True,
                            enable_dns_support=True)
        
        internet_gateway = ec2.CfnInternetGateway(self, 'InternetGateway')

        #this construct attaches the IGW to the VPC
        ec2.CfnVPCGatewayAttachment(self, 'IgwAttachment',
                                    vpc_id = my_vpc.ref,
                                    internet_gateway_id = internet_gateway.attr_internet_gateway_id)
        
        # Dictionary of subnets
        my_subnets = [
            # public subnets
            { 'cidr_block': '10.0.0.0/24', 'public':True },
            { 'cidr_block': '10.0.1.0/24', 'public':True },
            # private subnets
            { 'cidr_block': '10.0.2.0/24', 'public':False },
            { 'cidr_block': '10.0.3.0/24', 'public':False },
        ]

        # Create subnets in a loop
        for i, subnet in enumerate(my_subnets):
            subnet_resource = ec2.CfnSubnet(self, f'Subnet{i+1}',
                                            vpc_id=my_vpc.attr_vpc_id,
                                            cidr_block=subnet['cidr_block'],
                                            map_public_ip_on_launch=subnet['public'],
                                            # this uses available AZs for the subnets and matches the subnets to the AZs, based on even indeces
                                            availability_zone=Stack.availability_zones.fget(self)[i%2])
            
            # Create route tables for each subnet
            route_table = ec2.CfnRouteTable(self, f'Subnet{i+1}RouteTable{i+1}',
                                            vpc_id=my_vpc.attr_vpc_id)
            
            # Associate the route table with the subnet
            ec2.CfnSubnetRouteTableAssociation(self, f'Subnet{i+1}RouteTableAscn',
                                               route_table_id=route_table.attr_route_table_id,
                                               subnet_id=subnet_resource.attr_subnet_id)

            # Create a route for internet traffic to the IGW
            # if the subnet is public, add a route to the internet gateway to route internet traffic to the IGW
            if subnet['public']:

                ec2.CfnRoute(self, f'Subnet{i+1}InternetRoute',
                               route_table_id=route_table.attr_route_table_id,
                               destination_cidr_block='0.0.0.0/0',
                               gateway_id=internet_gateway.attr_internet_gateway_id)

            
