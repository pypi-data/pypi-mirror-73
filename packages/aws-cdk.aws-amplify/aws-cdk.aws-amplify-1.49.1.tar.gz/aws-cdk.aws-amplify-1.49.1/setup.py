import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-amplify",
    "version": "1.49.1",
    "description": "The CDK Construct Library for AWS::Amplify",
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
        "aws_cdk.aws_amplify",
        "aws_cdk.aws_amplify._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_amplify._jsii": [
            "aws-amplify@1.49.1.jsii.tgz"
        ],
        "aws_cdk.aws_amplify": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.7.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-codebuild==1.49.1",
        "aws-cdk.aws-codecommit==1.49.1",
        "aws-cdk.aws-iam==1.49.1",
        "aws-cdk.aws-kms==1.49.1",
        "aws-cdk.aws-secretsmanager==1.49.1",
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
