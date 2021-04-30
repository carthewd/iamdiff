import sys

from setuptools import setup, find_packages


install_requires = [
    'boto3==1.11.0',
    'botocore==1.14.0',
    'docutils==0.15.2',
    'jmespath==0.9.4',
    'python-dateutil==2.8.1',
    's3transfer==0.3.0',
    'six==1.13.0',
    'urllib3==1.25.8'
]

setup(
    name='iamdiff',
    version='0.1',
    url='https://github.com/carthewd/iamdiff',
    license='MIT',
    author='carthewd',
    author_email='donovan.carthew@gmail.com',
    description='iamdiff is a simple tool to create diffs of AWS IAM access that has been created vs what is actually used, leverage IAM Access Advisor.',
    long_description='iamdiff is a simple tool to create diffs of AWS IAM access that has been created vs what is actually used, leverage IAM Access Advisor.',
    keywords="aws iam access advisor",
    packages=find_packages(),
    platforms='any',
    install_requires=install_requires,
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': [
            'iamdiff = iamdiff.core:main',
        ]
    },
    zip_safe=False
)
