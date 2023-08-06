# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spoqa_aws_xray_flask_middleware']
install_requires = \
['aws-xray-sdk>=2.6.0,<3.0.0', 'flask>=0.10']

setup_kwargs = {
    'name': 'spoqa-aws-xray-flask-middleware',
    'version': '0.1.0',
    'description': 'Spoqa flavoured AWS X-Ray middleware for Flask',
    'long_description': "# spoqa-aws-xray-flask-middleware\n\nSpoqa flavoured AWS X-Ray middleware for Flask\n\n**Before**:\n\n```\nhttps://example.com/api/12345/messages\nhttp://localhost:8000/api/32123/messages\nhttp://127.0.0.1/api/43434/messages\n...\n```\n\n**After**:\n\n```\n//service_name/api/<int:id>/messages\n```\n\n## Usage\n\nReplace `aws_xray_sdk.ext.flask.middleware.XRayMiddleware` with `spoqa_aws_xray_flask_middleware.XRayMiddleware`\n\n```python\nfrom aws_xray_sdk.core import xray_recorder\nfrom spoqa_aws_xray_flask_middleware import XRayMiddleware\n\napp = Flask(__name__)\n\nxray_recorder.configure(service='fallback_name', dynamic_naming='*mysite.com*')\nXRayMiddleware(app, xray_recorder)\n```\n",
    'author': 'Spoqa Creators',
    'author_email': 'dev@spoqa.com',
    'maintainer': 'rusty',
    'maintainer_email': 'rusty@spoqa.com',
    'url': 'https://github.com/spoqa/aws-xray-flask-middleware',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
