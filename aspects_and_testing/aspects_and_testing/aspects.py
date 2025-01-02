import jsii # This import is needed for cdk aspects!!!
from aws_cdk import (
    IAspect,
    Stack,
    Annotations,
    aws_ec2 as ec2,
)

@jsii.implements(IAspect)
class EC2InstanceTypeChecker:

    def visit(self, node):
        
        if isinstance(node, ec2.CfnInstance):
            # Check if the instance type is not t2.micro or t3.micro. As anything else is outside of AWS free tier.
            if node.instance_type not in ['t2.micro', 't3.micro']:
                # Add a warning if the instance type is not t2.micro or t3.micro, the instance type is not within AWS free tier and therefor invalid.
                Annotations.of(node).add_warning(f'{node.instance_type} instance type is invalid')

                node.instance_type='t2.micro' # Automatic fix to replace the invalid instance type with t2.micro.


@jsii.implements(IAspect)
class SSHAnywhereChecker:
    # Check to see if the security group allows SSH access from anywhere (internet). If it does, add an error stating that this is not allowed.
    def visit(self, node):

        if isinstance(node, ec2.CfnSecurityGroup):
            
            rules = Stack.of(node).resolve(node.security_group_ingress)

            for rule in rules:

                if rule['ipProtocol'] == 'tcp' and rule ['fromPort'] <= 22 and rule['toPort'] >= 22:

                    if rule['CidrIp'] == '0.0.0.0/0':

                        Annotations.of(node).add_error('SSH access from anywhere is not allowed!')




            