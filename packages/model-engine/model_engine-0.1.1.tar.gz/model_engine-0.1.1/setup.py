#  Copyright 2020 BlueChasm LLC dba OsmosisAI.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open('VERSION', 'r') as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name='model_engine',
    version=version,
    packages=setuptools.find_packages(),
    url='https://github.com/osmosisai/modelengine',
    author='OsmosisAI, Inc.',
    author_email='contact@osmosisai.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'tensorflow>=2.2.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
