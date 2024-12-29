import aws_cdk as core
import aws_cdk.assertions as assertions

from serverless_app_l2.serverless_app_l2_stack import ServerlessAppL2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in serverless_app_l2/serverless_app_l2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ServerlessAppL2Stack(app, "serverless-app-l2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
