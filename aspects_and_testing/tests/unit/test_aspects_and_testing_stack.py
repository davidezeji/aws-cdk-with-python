import aws_cdk as core
import aws_cdk.assertions as assertions

from aspects_and_testing.my_sample_app_stack import MySampleAppStack
from aspects_and_testing.network_stack import NetworkStack

# check that the network stack has the correct number of resources (ex: VPCs, nat gateways)
def test_network_stack_resource_counts():
    app = core.App()

    root_stack = core.Stack(app, 'RootStack')

    network_stack = NetworkStack(root_stack, 'NetworkStack')

    application_stack = MySampleAppStack(root_stack, "MySampleAppStack",
                    my_vpc=network_stack.vpc)
    
    template = assertions.Template.from_stack(network_stack)

    template = resource_count_is('AWS::EC2::VPC', 1) # Check for 1 VPC

    template = resource_count_is('AWS::EC2::NatGateway', 0) # Ensure there are 0 NAT Gateways

def test_application_stack_web_server():
    app = core.App()

    root_stack = core.Stack(app, 'RootStack')

    network_stack = NetworkStack(root_stack, 'NetworkStack')

    application_stack = MySampleAppStack(root_stack, "MySampleAppStack",
                    my_vpc=network_stack.vpc)
    
    template = assertions.Template.from_stack(application_stack)

    template.has_resource_properties('AWS::EC2::Instance', {
        'InstanceType': assertions.Match.string_like_regexp('(t2|t3).micro'), # ensure the instance type is either t2.micro or t3.micro
        'ImageId': assertions.Match.any_value(),
        'KeyName': assertions.Match.absent() # ensure there are no key pairs created for the instance
    })

# Tests for more complex things such as arrays & Object Matchers found in your cloudformation templates

def test_web_server_security_group():
    app = core.App()

    root_stack = core.Stack(app, 'RootStack')

    network_stack = NetworkStack(root_stack, 'NetworkStack')

    application_stack = MySampleAppStack(root_stack, "MySampleAppStack",
                    my_vpc=network_stack.vpc)
    
    template = assertions.Template.from_stack(application_stack)

    template.has_resource_properties('AWS::EC2::SecurityGroup', {
        'SecurityGroupIngress': assertions.Match.array_equals([
            assertions.Match.object_like({
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'CidrIp': '0.0.0.0/0'
            })
        ])
    })