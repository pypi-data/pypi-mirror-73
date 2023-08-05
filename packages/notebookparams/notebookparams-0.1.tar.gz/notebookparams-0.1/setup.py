from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='notebookparams',
version='0.1',
description='Provide parameters to notebooks',
url='https://github.com/mccoy04041991/CampaignContributionDemoCode',
author='Sachin Sharma',
author_email='sasharma@aimconsulting.com',
license='MIT',
packages=['notebookparams'],
zip_safe=False)