from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2  # Duration,
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_rds as rds
from constructs import Construct


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # define a VPC with default configuration
        vpc = ec2.Vpc(
            self,
            "gsb-vpc",
            max_azs=2,  # This will create a VPC spanning 2 availability zones - chatgpt
            nat_gateways=0,
            enable_dns_hostnames = True,
            enable_dns_support = True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name = 'gsb-public',
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 20
                ),
                ec2.SubnetConfiguration(
                    name = 'gsb-isolated',
                    subnet_type = ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask = 20
                ),
            ],
        )

        ses_vpc_endpoint = ec2.InterfaceVpcEndpoint(
            self, "SesVpcEndpoint",
            vpc=vpc,
            service=ec2.InterfaceVpcEndpointService(
                "com.amazonaws.eu-west-2.email-smtp"  # Replace 'us-east-1' with your region
            ),
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),  # Choose private subnets
            private_dns_enabled=True  # Enable private DNS for SES endpoint
        )


        gsb_db = rds.DatabaseInstance(self,
                                        "GSB-Postgres",
                                        engine= rds.DatabaseInstanceEngine.POSTGRES,
                                        vpc=vpc,
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_type= ec2.SubnetType.PRIVATE_ISOLATED,
                                        ),
                                        credentials=rds.Credentials.from_generated_secret("gsb-lambda"),
                                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),
                                        port=5432,
                                        allocated_storage=20,
                                        multi_az= False,
                                        deletion_protection= False,
                                        publicly_accessible= True
                                    )

        gsb_db.secret.secret_arn


        gsb_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="TicketingLambda",
            environment= {
                'POSTGRES_USER' : secret.secret_value_from_json("username").to_string(),
            }
            function_name="GSB_TicketingLambda",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="../app/"
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                            subnet_type= ec2.SubnetType.PRIVATE_ISOLATED,
                        ),
        )

