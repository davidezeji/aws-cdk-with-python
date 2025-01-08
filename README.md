# AWS CDK With Python
[Udemy Course Reference](https://www.udemy.com/course/aws-cdk-with-python-step-by-step)
## What You Need to Install Locally to Run AWS CDK
* AWS CLI 
* Latest version of Node.js
* Install cdk toolkit via nodejs
* Python & pip

## How to Initialize a CDK Environmnet in AWS
* What does it mean to initialize a CDK environment?
    * It means that you are preparing an AWS region in your aws account for cdk deployments by creating necessary resources, like S3 buckets and IAM roles.
    * The 'cdk bootstrap' command is used to bootstrap a CDK environment (command format: 'cdk bootstrap <AWSACCOUNT#>/awsregion'): `cdk bootstrap 682033486371/us-east-1`    
        * this bootstraps your specified account in us-east-1, you can add on more accounts/regions in linear fashion to this command to bootstrap multiple environments at once, just make sure you have configured your aws cli locally before running this command.
    * Once the bootrap has been completed, go to your aws console and loock at stacks in cloudformation to see your newly created CDKToolkit (name is subject to change). Now you can use CDK in this aws environment.

## How to Initialize a CDK Folder
* CDK allows you to quickly set up your cdk resources by using the `cdk init` command (typing this command alone will show you a list of options). This helps you to quickly create templates for a CDK application and constructs. For example in the 'my_first_cdk_app' folder we set that folder up using the command `cdk init sample-app --language python`. This command creates all the necessary files and folders in this directory to create a CDK application with some constructs.

* Install requirements for python virtual environment after initialization 
    * **Why is this necessary?**: Different projects might require different versions of the same library. A virtual environment ensures that each project has its own set of dependencies, avoiding version conflicts. For example, one project might need Django 3.0, while another might require Django 4.0. Without a virtual environment, installing a new version of Django for one project could break the other.Installing packages globally on your system might cause conflicts with system tools or libraries. By using virtual environments, the global Python environment remains untouched, and your projects remain isolated.

**Steps:**
* Make sure you're in the correct directory
* set up python virtual environment: `python3 -m venv .venv` & `source .venv/bin/activate` (you should see (.venv) as the first item on your line to show you are in a virtual environment)
    * *if you misconfigured your python virtual environment delete it using: 'rm -rf .venv' in your project folder.*
* pip may not be updated in your virtual environment as you have it set up globally so upgrade pip in your environment: `python3 -m pip install --upgrade pip`
* install the requirements laid out in the 'requirements.txt' file in your directory: `pip install -r requirements.txt` (you can see their installation under the lib folder in your directory)

## Synthesize your CDK Code
The `cdk synth` command in the AWS Cloud Development Kit (CDK) generates an AWS CloudFormation template from your CDK application code. It translates the high-level constructs, configurations, and logic defined in your CDK code into the JSON or YAML format that CloudFormation uses to provision and manage AWS resources.

**Steps:**
* enter python virtual environment in your directory: `python3 -m venv .venv` & `source .venv/bin/activate` 
* type this command: 'cdk synth STACK_NAME' (ex: `cdk synth my-first-cdk-app`, keep in mind in you can enter multiple stack names in this one command). When no stack name is provided it synthesizes all stacks in your app.
    * the stack name for this example was found in is app.py on the root level directory of 'my_first_cdk_app folder'. **ALL STACK NAMES THAT YOU PLAN TO DEPLOY MUST BE DEFINED IN THIS FILE OR ELSE THEY WILL NOT GET DEPLOYED**
    * The actual python code creating the resources is found under the 'my_first_cd_app' folder in 'my_first_cd_app.py'
* After this command, a new folder called 'cdk.out' will be created which will have the cloudformation templates and other files.

## Deploy Your Code
**Using the command 'cdk deploy' does the job of both synthesizing your python code into cloudformation templates and deploying them into AWS.** Think of 'cdk synth' as similar to 'terraform plan' (plans but does not create resources), whereas 'cdk deploy' is similar to terraform apply (both plans AND creates resources).

Steps:
* Go to project folder
* Initialize python virtual environment: `python3 -m venv .venv` & `source .venv/bin/activate`
* Deploy cloudformation stacks: `cdk deploy STACKNAME` (you can define multiple stack names), to deploy all defined stacks use, `cdk deploy --all`
* Type 'y' when prompted to approve deployment
* Check cloudformation in aws console to see the created stack (look at resources section of your stack to see the AWS resources it created).

## Destroy Your CDK Stack
**IMPORTANT**: Make sure to never destroy your 'CDKToolkit' clouformation stack as it allows cdktoolkit to interact with your aws environment.

Steps:
* Go to project folder 
* Initialize python virtual environment: `python3 -m venv .venv` & `source .venv/bin/activate`
* Run cdk destroy command: `cdk destroy STACKNAME` (ex: 'cdk destroy MyFirstCdkAppStack') or just use `cdk destroy` to destroy all stacks in your directory.
* Type 'y' to proceed with deletion.
* Go to aws to ensure all resources/stacks have been destroyed.

### How to Delete Individual Constructs/Resources, Without Deleting the Entire Stack:

If you delete specific constructs/items in your files and then use the command 'cdk deploy' INSTEAD of 'cdk destroy', the cdk toolkit will recognize a difference in configuration and delete the resources no longer defined in your file to ensure a one-to-one relationship between your local and remote environments.

## Creating CDK Constructs
**Find L1 & L2 Constructs here:**

* [AWS CDK Construct Library](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)

**Find L3 constructs here:**
* [AWS Solutions Constructs](https://docs.aws.amazon.com/solutions/latest/constructs/welcome.html) (on the left hand side click on the 'API Reference' dropdown)
* [Construct Hub](https://constructs.dev/) (search for the constructs you're interested in and make sure to filter results on the left hand side of your search results)


**What are CDK Constructs?**

* CDK constructs are the basic building blocks of CDK applications. A construct refers to one or more AWS resources that are configured as a single component.
* There are three levels of constructs from lowest to highest level of encapsulation: L1, L2 and L3.
* Documentation for CDK constructs can found in the CDK constructs library (see above).

**What are L1 constructs?**
* These are the lowest level cdk contructs, mapping aws cloudformation resource types and properties one-to-one.
* Their names start with *'Cfn'* in the Construct library
* You can switch from CloudFormation's JSON or YAML templates to CDK code using only L1 constructs.

**What are L2 constructs?**
* These constructs provide sensible defaults for AWS resources, unlike L1 constructs, you don't have to know and provide all details of the underlying resources to configure them.
* They provide helpful instance methods to grant permissions, get metrics, configure networking, etc.
* They utilize L1 constructs to create the resources.
* In the CDK Construct library, they are the ones NOT prefixed with Cfn.
* *Using L2 constructs is recommended whenever possible, due to their ease of use.*

**What are L3 constructs?**
* These are also known as 'cdk patterns'
* These are the highest-level constructs, composed of resources from multiple services to create a complete solution (think of a module containing multiple services/resources)
* They include a mixture of L1 and L2 constructs.
* Not included in the CDK construct library but are imported as separate libraries in your programming language (imported at the top of your files, look at examples in the documentaion pages above).



### How to Create L1 Constructs
```
Example L1 constructs can be found in the 'my_sample_app_l1'folder.

This cdk app creates a VPC with two AZ's, 2 public/private subnets, internet gateway and route tables (nat gateways were not created as they are not covered by AWS' free tier limit).
```
**Steps:**
* Go to the correct project directory (this was initialized using the steps above)
* Go to your constructs file which is usually found under the sub-folder that contains your stack name and the file should be your stack name ending in .py (in this repository it is **aws-cdk-with-python/my_sample_app/my_sample_app/my_sample_app_stack.py**).
* Before you define a construct, find the aws-cdk-lib module and import it (note how 'aws_ec2 as ec2' is imported in the sample repository, in order to create VPC's and other resources).
* To specifically find L1 constructs in the library, select the correct resource name on the left side of the screen, scroll down on the left side until you find the 'CloudFormation Resources' section. Note how all the resources start with 'Cfn', showing how they relate to L1 constructs.
* When you've clicked the link of the resource you want to create, click the appropriate link for the programming language you plan to create the construct with.
* Define your constructs under `'def __init__'` with proper indentation.
* Once you've created your constructs, Initialize python virtual environment: `python3 -m venv .venv` & `source .venv/bin/activate`
* Synthesize your code: `cdk synth STACKNAME` (look for errors and check 'cdk.out' folder for generated cloudformation templates)
    * **Note:** In your virtual environment, you might need to run `pip install aws-cdk-lib constructs` to recognize the packages installed.


### How to Create L2 Constructs

```
Example L2 constructs can be found in the 'my_sample_app_l2' and 'serverless_app_l2' folders. 

my_sample_app_l2_stack.py: This cdk app creates a VPC with two AZ's, 2 public/private subnets, internet gateway and route tables (nat gateways were not created as they are not covered by AWS' free tier limit).

serverless_app_l2_stack.py & product_list_function.py: This cdk app creates a dynamodb table that includes a  with a lambda function which scans all items in the table and returns them as a list (this specfic lambda function can be found in 'product_list_function.py'), and can be accessed via a lambda url (once you click the url it invokes the lambda function which retrieves the contents of the dynamodb table as a list).
```
**Steps:**
* Go to the correct project directory (this was initialized using the steps above)
* Go to your constructs file which is usually found under the sub-folder that contains your stack name and the file should be your stack name ending in .py (in this repository it is **aws-cdk-with-python/my_sample_app/my_sample_app/my_sample_app_l2_stack.py**).
* Before you define a construct, find the aws-cdk-lib module and import it (note how 'aws_ec2 as ec2' is imported in the sample repository, in order to create VPC's and other resources).
* When you've clicked the link of the resource you want to create, click the appropriate link for the programming language you plan to create the construct with.
* Define your constructs under `'def __init__'` with proper indentation.
* Once you've created your constructs, Initialize python virtual environment: `python3 -m venv .venv` & `source .venv/bin/activate`
* Synthesize your code: `cdk synth STACKNAME` (look for errors and check 'cdk.out' folder for generated cloudformation templates)
    * **Note:** In your virtual environment, you might need to run `pip install aws-cdk-lib constructs` to recognize the packages installed.

### How to Create L3 Constructs

```
Example L3 constructs can be found in the 'my_sample_app_l3'folder. 

This cdk app creates a VPC with two AZ's, 2 public/private subnets, internet gateway and route tables (nat gateways were not created as they are not covered by AWS' free tier limit).
```
**Steps:**
* Go to the correct project directory (this was initialized using the steps above)
* Before you can use an L3 construct (aka cdk pattern), you must first install it in your python virtual environment. This means adding the package name into your 'requirements.txt' file. 
    * you can find this package name in constructhub under the reference documentation for the module you want to use (example package name: 'aws_solutions_constructs.aws_lambda_dynamodb', find the appropriate version at the top of the page next to the package name).
        * see example of this in 'requirements.txt' of the serverless_app_l3 folder.
    * make sure to install the package after adding it into requirements.txt by using the command 'pip3 install -r requirements.txt' (if you see an error in this process it's probably because there's an updated version of the package you are trying to install).
* Go to your constructs file which is usually found under the sub-folder that contains your stack name and the file should be your stack name ending in .py (in this repository it is **aws-cdk-with-python/my_sample_app/my_sample_app/my_sample_app_l3_stack.py**).
* Before you define a construct, find the aws-cdk-lib module and import it (note how 'aws_ec2 as ec2' is imported in the sample repository, in order to create VPC's and other resources).
* When you've clicked the link of the resource you want to create, click the appropriate link for the programming language you plan to create the construct with.
* Define your constructs under `'def __init__'` with proper indentation.
* Once you've created your constructs, Initialize python virtual environment: `python3 -m venv .venv` & `source .venv/bin/activate`
* Synthesize your code: `cdk synth STACKNAME` (look for errors and check 'cdk.out' folder for generated cloudformation templates)
    * **Note:** In your virtual environment, you might need to run `pip install aws-cdk-lib constructs` to recognize the packages installed.

## CDK Outputs
* Take a look a the 'serverless_app_l2_stack.py' file for an example of how to configure outputs. The point of doing this is to see outputs when you create a cloudformation console (ex: in this example, seeing the url of the lambda function that get's created).
    * notice how outputs are created using L1 constructs as seen by its naming 'CfnOutput' in the 'serverless_app_l2_stack.py' file. 
    * you can look at the 'outputs' tab of your cloudformation stack in aws to see generated outputs.

## Using AWS Cloudwatch to Collect Metrics & Errors from Constructs
* Take a look a the 'serverless_app_l2_stack.py' file for an example of how to configure cloudwatch metrics generated from your constructs.
    * In the example for this file, we collect the error metrics generated from the lambda function.
    * to generate an cloudwatch alarm, please comment out line 36 in the 'serverless_app_l2_stack.py' file and try accessing the lambda url seen in cloudwatch outputs for the corresponding stack. This will error and produce a cloudwatch alarm after a couple minutes.

## Configuring Networking & Assets on AWS CDK

In the networking folder, there is an example of a vpc, ec2 instance, Elastic IP, DB (RDS instance) and s3 bucket. with security groups for inbound/outbound connections. Please look ath the comments in 'networking_stack.py' for more details

### What are CDK Assets?

```
In the 'networking_stack.py' file we use an example of using s3 assets to update our website cert for our webserver instance (s3 asset (file) can be found in the index.html under the web_pages directory).
```

* CDK assets are local files, directories, or docker images on your computer that can be bundled into your cdk applications or libraries.
    * for example, our lambda function construct used s3 assets to bundle the code.

* **Amazon S3 Assets:** Used to budndle local files or directories and upload them to Amazon S3. This is supported by the 'aws_s3_assets' package of the CDK Construct library.
    * keep in mind, for directories they must first be compressed into zip packages before they can be uploaded.

* **Docker Image Assets:** Used to bundle local Docker images and upload them to Amazon ECR. This is supported by the 'aws_ecr_assets' package of the CDK Construct Library.

## Cross-stack References

Cross-stack references configure a multi-stack architecture where a stack references another stack's resources.

[How to use cross-stack references](https://www.udemy.com/course/aws-cdk-with-python-step-by-step/learn/lecture/37619238#overview)

## Nested-stacks 

Nested-stacks are a multi-stack architecture where a stack creates other stacks.

[How to use nested-stacks](https://www.udemy.com/course/aws-cdk-with-python-step-by-step/learn/lecture/37619242#overview)

## Tagging your CDK Constructs

See an example of tagging CDK constructs in the app.py file in the 'aspects_and_testing' folder and at the bottom of 'my_sample_app_stack.py'.

## CDK Aspects
```
Look at 'aspects.py' in the 'aspects_and_testing' folder for examples of aspects. The created aspects get imported in 'app.py'.
```

What are CDK aspects?
* They are used to apply an operation to each construct in a given scope.
* Most popular use case for CDK aspects: performing compliance checks on constructs. 

How do aspects work?
* Aspects employ the visitor-design-pattern in object-oriented programming.
* The aspect class implements the visit() method called for each construct during the preparation phase in the CDK app lifecycle.
* The visit() method gets the construct visited as input, the node argument, which you make comparisons or changes.

## Testing Your CDK Constructs

```
Look at the 'test_aspects_and_testing_stack.py' file for examples of unit tests.
```
You can write unit tests for your cdk apps by using *fine-grained assertions*:
* Fine-grained assertions is unit testing the contents of the synthesized CloudFormation template with test assertions.
* They enable you to test resource counts, expected resource properties, etc.
* With them, you can apply test-driven development by writing your tests before the code.
* fine-grained assertions are the most used and recommended way to test cdk apps.

To run tests, follow these steps:
* Go to appropriate directory
* initiate python virtual environment (`python3 -m venv .venv` & `source .venv/bin/activate`)
* install pytest from the requirements-dev.txt file: `pip install -r requirements-dev.txt`
* now you can use the pytest library to write new tests (place your test under the 'tests' folder. This folder gets created when you initialize a new cdk folder as seen in the steps above). Best practice is to create at least one test for each stack. 
* Write your tests
* use the command `pytest` on the command line to run the tests


