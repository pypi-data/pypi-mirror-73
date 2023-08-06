# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soccer_xg', 'soccer_xg.ml']

package_data = \
{'': ['*'], 'soccer_xg': ['models/*']}

install_requires = \
['betacal>=0.2.7,<0.3.0',
 'category_encoders>=2.2.2,<3.0.0',
 'click>=7.0,<8.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'ipykernel>=5.1,<6.0',
 'matplotlib>=3.1,<4.0',
 'matplotsoccer>=0.0.8,<0.0.9',
 'numpy>=1.18,<2.0',
 'pandas>=1.0,<2.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests>=2.23,<3.0',
 'scikit-learn>=0.22.1,<0.23.0',
 'seaborn>=0.10.0,<0.11.0',
 'socceraction>=0.2.1,<0.3.0',
 'tables>=3.6,<4.0',
 'understat>=0.1.2,<0.2.0',
 'xgboost>=1.0,<2.0']

extras_require = \
{'dask': ['dask[array,distributed,dataframe]>=2.15.0,<3.0.0',
          'dask_ml>=1.3.0,<2.0.0',
          'asyncssh>=2.2.1,<3.0.0',
          'paramiko>=2.7.1,<3.0.0']}

setup_kwargs = {
    'name': 'soccer-xg',
    'version': '0.0.1',
    'description': 'Train and analyse xG models on soccer event stream data',
    'long_description': '<div align="center">\n\t<h1>Soccer xG</h1>\n  <p><b>A Python package for training and analyzing expected goals (xG) models in soccer.</b></p>\n\t<img src="images/hero.png" width="600px">\n\t<br>\n\t<br>\n\t<br>\n</div>\n\n## About\n\nThis repository contains the code and models for our series on the analysis of xG models:\n\n- [How data availability affects the ability to learn good xG models](https://dtai.cs.kuleuven.be/sports/blog/how-data-availability-affects-the-ability-to-learn-good-xg-models)\n- [Illustrating the interplay between features and models in xG](https://dtai.cs.kuleuven.be/sports/blog/illustrating-the-interplay-between-features-and-models-in-xg)\n- [How data quality affects xG](https://dtai.cs.kuleuven.be/sports/blog/how-data-quality-affects-xg)\n\nIn particular, it contains code for experimenting with an exhaustive set of features and machine learning pipelines for predicting xG values from soccer event stream data. Since we rely on the [SPADL](https://github.com/ML-KULeuven/socceraction) language as input format, `soccer_xg` currently supports event streams provided by Opta, Wyscout, and StatsBomb. \n\n## Getting started\n\nThe recommended way to install `soccer_xg` is to simply use pip:\n\n```sh\n$ pip install soccer_xg\n```\n\nSubsequently, a basic xG model can be trained and applied with the code below:\n\n```python\nfrom itertools import product\nfrom soccer_xg import XGModel, DataApi\n\n# load the data\nprovider = \'wyscout_opensource\'\nleagues = [\'ENG\', \'ESP\', \'ITA\', \'GER\', \'FRA\']\nseasons = [\'1718\']\napi = DataApi([f"data/{provider}/spadl-{provider}-{l}-{s}.h5" \n        for (l,s) in product(leagues, seasons)])\n# load the default pipeline\nmodel = XGModel()\n# train the model\nmodel.train(api, training_seasons=[(\'ESP\', \'1718\'), (\'ITA\', \'1718\'), (\'GER\', \'1718\')])\n# validate the model\nmodel.validate(api, validation_seasons=[(\'ENG\', \'1718\')])\n# predict xG values\nmodel.estimate(api, game_ids=[2500098])\n```\n\nAlthough this default pipeline is suitable for computing xG, it is by no means the best possible model. \nThe notebook [`4-creating-custom-xg-pipelines`](./notebooks/4-creating-custom-xg-pipelines.ipynb) illustrates how you can train your own xG models or you can use one of the four pipelines used in our blogpost series. These can be loaded with:\n\n```python\nXGModel.load_model(\'openplay_logreg_basic\')\nXGModel.load_model(\'openplay_xgboost_basic\')\nXGModel.load_model(\'openplay_logreg_advanced\')\nXGModel.load_model(\'openplay_xgboost_advanced\')\n```\n\nNote that these models are meant to predict shots from open play. To be able to compute xG values from all shot types, you will have to combine them with a pipeline for penalties and free kicks. \n\n```python\nfrom soccer_xg import xg\n\nopenplay_model = xg.XGModel.load_model(f\'openplay_xgboost_advanced\') # custom pipeline for open play shots\nopenplay_model = xg.PenaltyXGModel() # default pipeline for penalties\nfreekick_model = xg.FreekickXGModel() # default pipeline for free kicks\n\nmodel = xg.XGModel()\nmodel.model = [openplay_model, openplay_model, freekick_model]\nmodel.train(api, training_seasons=...)\n```\n\n## For developers\n\n**Create venv and install deps**\n\n    make init\n\n**Install git precommit hook**\n\n    make precommit_install\n\n**Run linters, autoformat, tests etc.**\n\n    make pretty lint test\n\n**Bump new version**\n\n    make bump_major\n    make bump_minor\n    make bump_patch\n\n## License\n\nCopyright (c) DTAI - KU Leuven – All rights reserved.  \nLicensed under the Apache License, Version 2.0  \nWritten by [Pieter Robberechts](https://people.cs.kuleuven.be/~pieter.robberechts/), 2020\n',
    'author': 'Pieter Robberechts',
    'author_email': 'pieter.robberechts@cs.kuleuven.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/soccer_xg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
