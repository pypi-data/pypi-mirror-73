import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-appsync",
    "version": "1.49.1",
    "description": "The CDK Construct Library for AWS::AppSync",
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
        "aws_cdk.aws_appsync",
        "aws_cdk.aws_appsync._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_appsync._jsii": [
            "aws-appsync@1.49.1.jsii.tgz"
        ],
        "aws_cdk.aws_appsync": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.7.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cognito==1.49.1",
        "aws-cdk.aws-dynamodb==1.49.1",
        "aws-cdk.aws-iam==1.49.1",
        "aws-cdk.aws-lambda==1.49.1",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
