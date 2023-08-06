# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opoca',
 'opoca.data',
 'opoca.data.integrations',
 'opoca.evaluation',
 'opoca.features',
 'opoca.hyperparam_search',
 'opoca.models',
 'opoca.trainers']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.20,<0.30.0',
 'MonthDelta>=0.9.1,<0.10.0',
 'category_encoders>=2.2.2,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'dynaconf>=2.2.3,<3.0.0',
 'google-cloud-storage>=1.29.0,<2.0.0',
 'horology>=1.1.0,<2.0.0',
 'imbalanced-learn>=0.7.0,<0.8.0',
 'ipython>=7.16.1,<8.0.0',
 'joblib>=0.15.1,<0.16.0',
 'kubernetes>=11.0.0,<12.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'mlflow>=1.9.1,<2.0.0',
 'numpy>=1.19.0,<2.0.0',
 'optuna>=1.5.0,<2.0.0',
 'pandas-profiling>=2.8.0,<3.0.0',
 'pandas>=1.0.5,<2.0.0',
 'plotly>=4.8.1,<5.0.0',
 'pyarrow>=0.17.1,<0.18.0',
 'python-dateutil==2.8.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'quilt3>=3.1.14,<4.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scikit-optimize>=0.7.4,<0.8.0',
 'scipy>=1.5.0,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'simple-salesforce>=1.1.0,<2.0.0',
 'tqdm>=4.46.1,<5.0.0',
 'urllib3==1.24.3',
 'xgboost>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'opoca',
    'version': '0.1.0',
    'description': 'Opoca library aims to drastically speed up producing proof of concepts (PoC) for machine learning projects.',
    'long_description': None,
    'author': 'Apollo Team',
    'author_email': 'ml-team@netguru.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
