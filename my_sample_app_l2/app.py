#!/usr/bin/env python3

import aws_cdk as cdk

from my_sample_app_l2.my_sample_app_l2_stack import MySampleAppL2Stack


app = cdk.App()
MySampleAppL2Stack(app, "MySampleAppL2Stack")

app.synth()
