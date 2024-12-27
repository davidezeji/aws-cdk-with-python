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