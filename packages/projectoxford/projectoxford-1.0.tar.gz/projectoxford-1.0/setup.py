#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation
# All rights reserved.
#-------------------------------------------------------------------------

import os

NOTICE = os.path.join(os.path.abspath(__file__), '..', 'NOTICE.rst')
with open(NOTICE, 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup_cfg = dict(
    name='projectoxford',
    version='1.0',
    description='Deprecated Project Oxford SDK. Install `projectoxford<1` for legacy versions.',
    long_description=LONG_DESCRIPTION,
    author='Microsoft Corporation',
    author_email='python@microsoft.com',
    url='https://docs.microsoft.com/python/api/overview/azure/cognitive-services',
    packages=['projectoxford'],
)

from distutils.core import setup
setup(**setup_cfg)
