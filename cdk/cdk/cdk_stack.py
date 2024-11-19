from aws_cdk import Stack, CfnOutput, Duration
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_rds as rds
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_iam as iam
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
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

        sec_group = ec2.SecurityGroup(
            self, "LambdaSecGroup",
            vpc=vpc,
            allow_all_outbound=True,
        )

        ses_vpc_endpoint = ec2.InterfaceVpcEndpoint(
            self, "SesVpcEndpoint",
            vpc=vpc,
            service=ec2.InterfaceVpcEndpointAwsService.EMAIL_SMTP,
            # service=ec2.InterfaceVpcEndpointService("com.amazonaws.eu-west-2.email-smtp")
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),  # Choose private subnets
            private_dns_enabled=True,  # Enable private DNS for SES endpoint
            security_groups=[sec_group]
            
        )

        secrets_manager_vpc_endpoint = ec2.InterfaceVpcEndpoint(
            self, "SecretsMgrVpcEndpoint",
            vpc=vpc,
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            private_dns_enabled=True,
            security_groups=[sec_group]
        )

        


        gsb_db = rds.DatabaseInstance(self,
                                        "GSB-Postgres",
                                        engine= rds.DatabaseInstanceEngine.POSTGRES,
                                        vpc=vpc,
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_type= ec2.SubnetType.PRIVATE_ISOLATED,
                                        ),
                                        credentials=rds.Credentials.from_generated_secret("gsb_lambda"),
                                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),
                                        port=5432,
                                        allocated_storage=20,
                                        multi_az=False,
                                        deletion_protection=False,
                                        publicly_accessible=False,
                                        security_groups=[sec_group]
                                    )

        gsb_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="TicketingLambda",
            environment = {
                'AWS_SECRET_ARN' : gsb_db.secret.secret_arn
            },
            function_name="GSB_TicketingLambda",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="../app/"
            ),
            vpc=vpc,
            timeout=Duration.minutes(3),
            vpc_subnets=ec2.SubnetSelection(
                            subnet_type= ec2.SubnetType.PRIVATE_ISOLATED,
                        ),
            security_groups=[sec_group]
        )

        scanner_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="ScanningLambda",
            environment = {
                'AWS_SECRET_ARN' : gsb_db.secret.secret_arn
            },
            function_name="GSB_ScanningLambda",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="../scanner/"
            ),
            timeout=Duration.minutes(5),
            vpc=vpc,
            security_groups=[sec_group]
        )

        gsb_db.secret.grant_read(gsb_lambda)
        gsb_db.secret.grant_read(scanner_lambda)

        gsb_lambda.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        scanner_lambda.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )

        gsb_db.connections.allow_from(gsb_lambda, ec2.Port.tcp(5432))
        gsb_db.connections.allow_from(scanner_lambda, ec2.Port.tcp(5432))

        # Create an API Gateway endpoint for the Lambda
        gsb_api = apigateway.LambdaRestApi(
            self, "TicketingGateway",
            handler=gsb_lambda,
            proxy=True
        )

        # Create an API Gateway endpoint for the Lambda
        scanner_api = apigateway.LambdaRestApi(
            self, "ScannerGateway",
            handler=scanner_lambda,
            proxy=True
        )

        ticketing_hosted_zone = route53.HostedZone(
            self, "TicketingHostedZone",
            zone_name="ticketing.girtonspringball.com"
        )

        scanning_hosted_zone = route53.HostedZone(
            self, "ScanningHostedZone",
            zone_name="scanning.girtonspringball.com"
        )

        # 4. Create a certificate for the custom domain
        ticketing_certificate = acm.Certificate(
            self, "TicketingCertificate",
            domain_name="ticketing.girtonspringball.com",
            validation=acm.CertificateValidation.from_dns(ticketing_hosted_zone)
        )

        scanner_certificate = acm.Certificate(
            self, "ScanningCertificate",
            domain_name="scanning.girtonspringball.com",
            validation=acm.CertificateValidation.from_dns(scanning_hosted_zone)
        )

        # 5. Add a custom domain to the API Gateway
        ticketing_custom_domain = apigateway.DomainName(
            self, "TicketingDomain",
            domain_name="ticketing.girtonspringball.com",
            certificate=ticketing_certificate,
            endpoint_type=apigateway.EndpointType.REGIONAL # most traffic will be in the UK only
        )

        scanning_custom_domain = apigateway.DomainName(
            self, "ScanningDomain",
            domain_name="scanning.girtonspringball.com",
            certificate=scanner_certificate,
            endpoint_type=apigateway.EndpointType.REGIONAL # most traffic will be in the UK only
        )

        # 6. Map the custom domain to the API Gateway deployment
        apigateway.BasePathMapping(
            self, "TicketingBasePathMapping",
            domain_name=ticketing_custom_domain,
            rest_api=gsb_api,
            stage=gsb_api.deployment_stage  # Map the custom domain to the default stage
        )

        apigateway.BasePathMapping(
            self, "ScanningBasePathMapping",
            domain_name=scanning_custom_domain,
            rest_api=scanner_api,
            stage=scanner_api.deployment_stage  # Map the custom domain to the default stage
        )


        # 7. Add a Route 53 record for the custom domain
        route53.ARecord(
            self, "TicketingApiRecord",
            zone=ticketing_hosted_zone,
            target=route53.RecordTarget.from_alias(route53_targets.ApiGatewayDomain(ticketing_custom_domain))
        )

        route53.ARecord(
            self, "ScanningApiRecord",
            zone=scanning_hosted_zone,
            target=route53.RecordTarget.from_alias(route53_targets.ApiGatewayDomain(scanning_custom_domain))
        )

        # Output the API Gateway URL
        CfnOutput(self, "TicketingGatewayUrl", value=gsb_api.url)
        CfnOutput(self, "ScanningGatewayUrl", value=scanner_api.url)




