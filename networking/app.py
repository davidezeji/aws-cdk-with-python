#!/usr/bin/env python3

import aws_cdk as cdk

from networking.networking_stack import NetworkingStack


app = cdk.App()
NetworkingStack(app, "NetworkingStack")

app.synth()
