import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-lambda-destinations",
    "version": "1.49.1",
    "description": "CDK Destinations Constructs for AWS Lambda",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_lambda_destinations",
        "aws_cdk.aws_lambda_destinations._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_lambda_destinations._jsii": [
            "aws-lambda-destinations@1.49.1.jsii.tgz"
        ],
        "aws_cdk.aws_lambda_destinations": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.7.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-events==1.49.1",
        "aws-cdk.aws-events-targets==1.49.1",
        "aws-cdk.aws-lambda==1.49.1",
        "aws-cdk.aws-sns==1.49.1",
        "aws-cdk.aws-sqs==1.49.1",
        "aws-cdk.core==1.49.1",
        "constructs>=3.0.2, <4.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
