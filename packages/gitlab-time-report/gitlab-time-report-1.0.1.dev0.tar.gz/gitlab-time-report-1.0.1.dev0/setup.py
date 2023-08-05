# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlab_time_report']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'python-gitlab>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['gitlab-time-report = '
                     'gitlab_time_report.time_report:main']}

setup_kwargs = {
    'name': 'gitlab-time-report',
    'version': '1.0.1.dev0',
    'description': 'GitLab time reporting made easy.',
    'long_description': '# GitLab-time-report\n\nPlease visit the [Read the Docs](http://ifs.pages.ifs.hsr.ch/gitlab-time-report/gitlab-time-report/) documentation for more information.\n\n## Development\n\nPlease visit the [according documentation page](http://ifs.pages.ifs.hsr.ch/gitlab-time-report/gitlab-time-report/development/).\n',
    'author': 'Johannes Wildermuth',
    'author_email': 'johannes.wildermuth@hsr.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.dev.ifs.hsr.ch/ifs/gitlab-time-report/gitlab-time-report',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
