from setuptools import setup, find_packages
from simple_aws_lambda_maker import VERSION

# fmt: off

setup(
      name = "simple-aws-lambda-maker"
    , version = VERSION
    , packages = find_packages(include="simple_aws_lambda_maker.*")

    , python_requires = ">= 3.6"

    , install_requires =
      [ "delfick_project==0.7.5"

      , "boto3==1.14.16"
      , "datadiff==2.0.0"
      , "ruamel.yaml==0.16.10"
      , "requests==2.24.0"
      ]

    , entry_points =
      { 'console_scripts' :
        [ 'salm = simple_aws_lambda_maker.executor:main'
        ]
      }

    # metadata for upload to PyPI
    , url = "https://github.com/delfick/simple-aws-lambda-maker"
    , author = "Stephen Moore"
    , author_email = "github@delfick.com"
    , description = "Very simple deploy tool for aws lambda"
    , long_description = open("README.rst").read()
    , license = "MIT"
    , keywords = "aws lambda"
    )

# fmt: on
