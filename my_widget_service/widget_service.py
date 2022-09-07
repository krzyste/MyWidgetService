import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_lambda as lambda_,
)


class WidgetService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # lambdaLayer = lambda_.LayerVersion(
        #     self,
        #     "lambda-layer",
        #     code=lambda_.AssetCode("lambda_layers/layer/"),
        #     compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
        # )
        lambdaLayerAwsDataWrangler = lambda_.LayerVersion.from_layer_version_arn(
            self,
            "AWSDataWranglerLayer",
            "arn:aws:lambda:eu-west-1:336392948345:layer:AWSDataWrangler-Python39:7",
        )

        # arn:aws:lambda:eu-west-1:336392948345:layer:AWSDataWrangler-Python39:7
        handler_rn = lambda_.Function(
            self,
            "RandomNumber",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset(
                "resources",
                bundling=cdk.BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install --no-cache reverse_geocode -t /asset-output && cp -au . /asset-output",
                    ],
                    user="root",
                ),
            ),
            handler="random_number.lambda_handler",
            layers=[lambdaLayerAwsDataWrangler],
        )
        handler_hw = lambda_.Function(
            self,
            "HelloWorld",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("resources"),
            handler="hello_world.lambda_handler",
            layers=[lambdaLayerAwsDataWrangler],
            environment=dict(RANDOM_NUMBER_LAMBDA=handler_rn.function_arn),
        )

        api = apigateway.RestApi(
            self,
            "widgets-api",
            rest_api_name="Widget Service",
            description="This service serves widgets.",
        )
        get_hello = api.root.add_resource("get_hello")
        get_widgets_integration = apigateway.LambdaIntegration(
            handler_hw,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        get_hello.add_method("GET", get_widgets_integration)
