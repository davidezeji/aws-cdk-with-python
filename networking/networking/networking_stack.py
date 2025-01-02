from aws_cdk import (
    CfnOutput,
    RemovalPolicy, # by default CDK will not destroy DB resources by default, so we need to define this.
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_s3_assets as s3_assets # need to install to be able to use s3 assets
)
from constructs import Construct

class NetworkingStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creating a VPC without a NAT gateway.
        my_vpc = ec2.Vpc(self, 'MyVpc', 
                         nat_gateways=0)

        # Creating a web server instance in the public subnet
        web_server = ec2.Instance(self, 'WebServer', 
                                  machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                  instance_type=ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2,
                                                                    instance_size=ec2.InstanceSize.MICRO),
                                  vpc=my_vpc,
                                  vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                  user_data_causes_replacement=True)

        # Attaching an Elastic IP to keep the DNS name on updates
        ec2.CfnEIPAssociation(self, 'ElasticIP',
                              instance_id=web_server.instance_id)

        #Installing packages at instance launch
        web_server.add_user_data('yum update -y',
                                 'amazon-linux-extras install nginx1',
                                 'rm -rf /usr/share/nginx/html/*',) #deleting default html pages since i am adding a custom webpage using s3 assets below

        # Outputting the public DNS name of the web server
        CfnOutput(self, 'WebServerDnsName',
                 value=web_server.instance_public_dns_name)
        
        # Allowing connections to the web server from the internet
        web_server.connections.allow_from_any_ipv4(ec2.Port.tcp(80), 'Allow HTTP access from the Internet')
        #Allow SSH connections to the web server from the internet
        web_server.connections.allow_from_any_ipv4(ec2.Port.tcp(22), 'Allow SSH access from the Internet')

        # DB instance configuration
        db_instance = rds.DatabaseInstance(self, 'DbInstance',
                                           engine=rds.DatabaseInstanceEngine.MARIADB,
                                           vpc=my_vpc,
                                           # creating a private subnet for the DB instance
                                           vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                           instance_type=ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2,
                                                                             instance_size=ec2.InstanceSize.MICRO),
                                           # this ensures that the DB instance is deleted when the stack is deleted. BE CAREFUL ABOUT USING THIS CONFIGURATION IN PRODUCTION!!!
                                           removal_policy=RemovalPolicy.DESTROY)
        
        # Allowing inbound connections from the Web server to the DB instance
        db_instance.connections.allow_default_port_from(web_server, 'Allow MySQL access from the web server')

        # Installing MySQL client on the web server
        web_server.add_user_data('yum install mysql -y')

        # Outputting the DB endpoint
        CfnOutput(self, 'DbEndpoint',
                  value=db_instance.db_instance_endpoint_address)
        
        # Deploying a web page onto the web server using s3 assets
        web_page_asset = s3_assets.Asset(self, 'WebPageAsset', 
                                         path='web_pages/index.html')
        
        web_server.user_data.add_s3_download_command(bucket=web_page_asset.bucket,
                                                     bucket_key=web_page_asset.s3_object_key,
                                                     #this is where the downloaded file will be saved on the instance
                                                     local_file='/usr/share/nginx/html/index.html') 
    
        # Granting read access to the web server to the downloaded web page from S3 
        web_page_asset.grant_read(web_server.role)

        # Starting the Nginx service on the web server  (this will start the web server)
        web_server.add_user_data('service nginx start')
                                        
