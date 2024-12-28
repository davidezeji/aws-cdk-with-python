import aws_cdk as core
import aws_cdk.assertions as assertions
from my_sample_app_l2.my_sample_app_l2_stack import MySampleAppL2Stack


def test_sqs_queue_created():
    app = core.App()
    stack = MySampleAppL2Stack(app, "my-sample-app-l2")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = MySampleAppL2Stack(app, "my-sample-app-l2")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
