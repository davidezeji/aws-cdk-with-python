#!/usr/bin/env python3
import os

import aws_cdk as cdk

from my_sample_app.my_sample_app_stack import MySampleAppStack
from my_sample_app.network_stack import NetworkStack

# Add custom aspects
from my_sample_app.aspects import (EC2InstanceTypeChecker, SSHAnywhereChecker)


app = cdk.App()

root_stack = cdk.Stack(app, 'RootStack')

network_stack = NetworkStack(root_stack, 'NetworkStack')

application_stack = MySampleAppStack(root_stack, "MySampleAppStack",
                 my_vpc=network_stack.vpc)

# Aspect attachements
cdk.Aspects.of(root_stack).add(EC2InstanceTypeChecker())
cdk.Aspects.of(root_stack).add(SSHAnywhereChecker())

# Stack-level tagging
cdk.Tags.of(network_stack).add('category', 'network')
cdk.Tags.of(application_stack).add('category', 'application',
                                   priority=200)

app.synth()
