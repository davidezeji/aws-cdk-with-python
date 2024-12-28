# AWS CDK With Python
[Udemy Course Reference](https://www.udemy.com/course/aws-cdk-with-python-step-by-step)
## What You Need to Install Locally to Run AWS CDK
* AWS CLI 
* Latest version of Node.js
* Install cdk toolkit via nodejs
* Python & pip

## How to Initialize CDK Environmnet in AWS
* What does it mean to initialize a CDK environment?
    * It means that you are preparing an AWS region in your aws account for cdk deployments by creating necessary resources, like S3 buckets and IAM roles.
    * The 'cdk bootstrap' command is used to bootstrap a CDK environment (command format: 'cdk bootstrap awsaccount#/awsregion'): `cdk bootstrap 682033486371/us-east-1`    
        * this bootstraps your specified account in us-east-1, you can add on more accounts/regions in linear fashion to this command to bootstrap multiple environments at once, just make sure you have configured your aws cli locally before running this command.
    * Once the bootrap has been completed, go to your aws console and loock at stacks in cloudformation to see your newly created CDKToolkit (name is subject to change). Now you can use CDK in this aws environment.

## How to Initialize a CDK Folder
* CDK allows you to quickly set up your cdk resources by using the `cdk init` command (typing this command alone will show you a list of options). This helps you to quickly create templates for a CDK application and constructs. For example in the 'my_first_cdk_app' folder we set that folder up using the command `cdk init sample-app --language python`. This command creates all the necessary files and folders in this directory to create a CDK application with some constructs.

* Install requirements for python virtual environment after initialization 
    * **Why is this necessary?**: Different projects might require different versions of the same library. A virtual environment ensures that each project has its own set of dependencies, avoiding version conflicts. For example, one project might need Django 3.0, while another might require Django 4.0. Without a virtual environment, installing a new version of Django for one project could break the other.Installing packages globally on your system might cause conflicts with system tools or libraries. By using virtual environments, the global Python environment remains untouched, and your projects remain isolated.

**Steps:**
* Make sure you're in the correct directory
* set up python virtual environment: `source .venv/bin/activate` (you should see (.venv) as the first item on your line to show you are in a virtual environment)
* pip may not be updated in your virtual environment as you have it set up globally so upgrade pip in your environment: `python3 -m pip install --upgrade pip`
* install the requirements laid out in the 'requirements.txt' file in your directory: `pip install -r requirements.txt` (you can see their installation under the lib folder in your directory)

## Synthesize your CDK Code
The `cdk synth` command in the AWS Cloud Development Kit (CDK) generates an AWS CloudFormation template from your CDK application code. It translates the high-level constructs, configurations, and logic defined in your CDK code into the JSON or YAML format that CloudFormation uses to provision and manage AWS resources.

**Steps:**
* enter python virtual environment in your directory: `source .venv/bin/activate` 
* type this command: 'cdk synth STACK_NAME' (ex: `cdk synth my-first-cdk-app`, keep in mind in you can enter multiple stack names in this one command). When no stack name is provided it synthesizes all stacks in your app.
    * the stack name for this example was found in is app.py on the root level directory of 'my_first_cdk_app folder'. **ALL STACK NAMES THAT YOU PLAN TO DEPLOY MUST BE DEFINED IN THIS FILE OR ELSE THEY WILL NOT GET DEPLOYED**
    * The actual python code creating the resources is found under the 'my_first_cd_app' folder in 'my_first_cd_app.py'
* After this command, a new folder called 'cdk.out' will be created which will have the cloudformation templates and other files.

## Deploy Your Code
**Using the command 'cdk deploy' does the job of both synthesizing your python code into cloudformation templates and deploying them into AWS.** Think of 'cdk synth' as similar to 'terraform plan' (plans but does not create resources), whereas 'cdk deploy' is similar to terraform apply (both plans AND creates resources).

Steps:
* Go to project folder
* Initialize python virtual environment: `source .venv/bin/activate`
* Deploy cloudformation stacks: `cdk deploy STACKNAME` (you can define multiple stack names), to deploy all defined stacks use, `cdk deploy --all`
* Type 'y' when prompted to approve deployment
* Check cloudformation in aws console to see the created stack (look at resources section of your stack to see the AWS resources it created).

## Destroy Your CDK Stack
**IMPORTANT**: Make sure to never destroy your 'CDKToolkit clouformation stack as it allows cdktoolkit to interact with your aws environment.

Steps:
* Go to project folder 
* Initialize python virtual environment: `source .venv/bin/activate`
* Run cdk destroy command: `cdk destroy STACKNAME` (ex: 'cdk destroy MyFirstCdkAppStack') or just use `cdk destroy` to destroy all stacks in your directory.
* Type 'y' to proceed with deletion.
* Go to aws to ensure all resources/stacks have been destroyed.

## Creating CDK Constructs
[AWS CDK Construct Library](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)

**What are CDK Constructs?**

* CDK constructs are the basic building blocks of CDK applications. A construct refers to one or more AWS resources that are configured as a single component.
* There are three levels of constructs from lowest to highest level of encapsulation: L1, L2 and L3.
* Documentation for CDK constructs can found in the CDK constructs library (see above).

**What are L1 constructs?**
* These are the lowest level cdk contructs, mapping aws cloudformation resource types and properties one-to-one.
* Their names start with *'Cfn'* in the Construct library
* You can switch from CloudFormation's JSON or YAML templates to CDK code using only L1 constructs.

**What are L2 constructs?**
**What are L3 constructs?**

### How to Create L1 Constructs
```
Example L1 constructs can be found in the 'my_first_cdk_app'folder.

This cdk app creates a VPC with two AZ's, 2 public/private subnets, internet gateway and route tables (nat gateways were not created as they are not covered by AWS' free tier limit).
```
**Steps:**
* Go to the correct project directory
* Go to your constructs file which is usually found under the sub-folder that contains your stack name and the file should be your stack name ending in .py (in this repository it is **aws-cdk-with-python/my_sample_app/my_sample_app/my_sample_app_stack.py**).
* Before you define a construct, find the aws-cdk-lib module and import it (note how 'aws_ec2 as ec2' is imported in the sample repository, in order to create VPC's and other resources).
* To specifically find L1 constructs in the library, scroll down on the left side until you find the 'CloudFormation Resources' section. Note how all the resources start with 'Cfn', showing how they relate to L1 constructs.
* When you've clicked the link of the resource you want to create, click the appropriate link for the programming language you plan to create the construct with.
* Define your constructs under 'def __init__' with proper indentation.

### How to Create L2 Constructs
### How to Create L3 Constructs