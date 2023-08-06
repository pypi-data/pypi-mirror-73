import json
import setuptools

kwargs = json.loads("""
{
    "name": "mbonig.sqs-redrive",
    "version": "1.51.1",
    "description": "A redrive construct to use with an SQS queue and it's dead letter queue",
    "license": "MIT",
    "url": "https://github.com/mbonig/sqs-redrive",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/mbonig/sqs-redrive"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.sqs_redrive",
        "mbonig.sqs_redrive._jsii"
    ],
    "package_data": {
        "mbonig.sqs_redrive._jsii": [
            "sqs-redrive@1.51.1.jsii.tgz"
        ],
        "mbonig.sqs_redrive": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.22.0",
        "publication>=0.0.3",
        "aws-cdk.aws-lambda-nodejs>=1.51.0, <2.0.0-0",
        "aws-cdk.aws-sqs>=1.51.0, <2.0.0-0",
        "aws-cdk.core>=1.51.0, <2.0.0-0",
        "aws-cdk.region-info>=1.51.0, <2.0.0-0",
        "constructs>=3.0.4, <4.0.0-0"
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
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
