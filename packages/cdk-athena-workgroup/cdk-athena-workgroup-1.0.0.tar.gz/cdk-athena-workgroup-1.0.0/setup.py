import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-athena-workgroup",
    "version": "1.0.0",
    "description": "CDK Construct for creating Athena WorkGroups",
    "license": "Apache-2.0",
    "url": "https://github.com/udondan/cdk-athena-workgroup",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "project_urls": {
        "Source": "https://github.com/udondan/cdk-athena-workgroup.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_athena_workgroup",
        "cdk_athena_workgroup._jsii"
    ],
    "package_data": {
        "cdk_athena_workgroup._jsii": [
            "cdk-athena-workgroup@1.0.0.jsii.tgz"
        ],
        "cdk_athena_workgroup": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.8.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudformation>=1.50.0, <2.0.0",
        "aws-cdk.aws-iam>=1.50.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.50.0, <2.0.0",
        "aws-cdk.core>=1.50.0, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
        "iam-floyd>=0.20.0, <0.21.0"
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
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
