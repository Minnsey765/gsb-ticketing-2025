# this doesnt work if you unhash it but im putting it here bc i can't remember the command
# pip install aws-cdk-lib aws-cdk.core aws-cdk.aws_ec2

# libraries i think i need
import os

# get environment variables from the 'production.py' file
import production
from aws_cdk import aws_ec2 as ec2
from aws_cdk import core as cdk


class VpcStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # define a VPC with default configuration
        vpc = ec2.Vpc(
            self,
            "gsb-vpc",
            max_azs=2,  # This will create a VPC spanning 2 availability zones - chatgpt
            nat_gateways=1,  # Creates a NAT Gateway for outbound internet access - idk what this means tbh
        )

        # Outputs (Optional): You can output the VPC ID and Subnet IDs
        cdk.CfnOutput(self, "VpcId", value=vpc.vpc_id)
        for subnet in vpc.public_subnets:
            cdk.CfnOutput(
                self, f"PublicSubnet-{subnet.node.id}", value=subnet.subnet_id
            )


# Initialize the CDK App
app = cdk.App()

# Retrieve account and region from the production file
env = cdk.Environment(
    account=production.AWS_USER_ACCOUNT_ID, region=production.AWS_SES_REGION_NAME
)

# Instantiate the stack with environment settings
VpcStack(app, "VpcStack", env=env)

# Synthesize the CloudFormation template
app.synth()
