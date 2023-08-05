import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-time-bomb",
    "version": "1.50.0",
    "description": "Implode your AWS CDK Stack after set amount of time, save money, be happy!",
    "license": "MIT",
    "url": "https://github.com/jmb12686/time-bomb#readme",
    "long_description_content_type": "text/markdown",
    "author": "John Belisle<jmb186@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/jmb12686/time-bomb.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_time_bomb",
        "cdk_time_bomb._jsii"
    ],
    "package_data": {
        "cdk_time_bomb._jsii": [
            "cdk-time-bomb@1.50.0.jsii.tgz"
        ],
        "cdk_time_bomb": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.8.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-events>=1.50.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.50.0, <2.0.0",
        "aws-cdk.aws-iam>=1.50.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.50.0, <2.0.0",
        "aws-cdk.core>=1.50.0, <2.0.0"
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
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
