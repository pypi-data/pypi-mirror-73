# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['observ']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['test = scripts:main']}

setup_kwargs = {
    'name': 'observ',
    'version': '0.2.0',
    'description': '',
    'long_description': '[![PyPI version](https://badge.fury.io/py/observ.svg)](https://badge.fury.io/py/observ)\n[![CI status](https://github.com/Korijn/observ/workflows/CI/badge.svg)](https://github.com/Korijn/observ/actions)\n\n# Observ 👁\n\nObserv is a Python port of [Vue.js](https://vuejs.org/)\' [computed properties and watchers](https://vuejs.org/v2/guide/computed.html). It is completely event loop/framework agnostic and has no dependencies so it can be used in any project targeting Python >= 3.6.\n\nObserv provides the following two benefits for stateful applications:\n\n1) You no longer need to manually invalidate and recompute state (e.g. by dirty flags):\n    * computed state is invalidated automatically\n    * computed state is lazily re-evaluated\n2) You can react to changes in state (computed or not), enabling unidirectional flow:\n    * _state changes_ lead to _view changes_ (e.g. a state change callback updates a UI widget)\n    * the _view_ triggers _input events_ (e.g. a mouse event is triggered in the UI)\n    * _input events_ lead to _state changes_ (e.g. a mouse event updates the state)\n\n## API\n\n`from observ import observe, computed, watch`\n\n* `state = observe(state)`\n\nObserve nested structures of dicts, lists, tuples and sets. Returns an observable clone of the state input object.\n\n* `watcher = watch(func, callback, deep=False, immediate=False)`\n\nReact to changes in the state accessed in `func` with `callback(old_value, new_value)`. Returns a watcher object. `del`elete it to disable the callback.\n\n* `wrapped_func = computed(func)`\n\nDefine computed state based on observable state with `func` and recompute lazily. Returns a wrapped copy of the function which only recomputes the output if any of the state it depends on becomes dirty. Can be used as a function decorator.\n\n## Quick start and example\n\nInstall observ with pip/pipenv/poetry:\n\n`pip install observ`\n\nExample usage:\n\n```python\n>>> from observ import computed, observe, watch\n>>>\n>>> a = observe({"foo": 5})\n>>>\n>>> def my_callback(old_value, new_value):\n...     print(f"{old_value} became {new_value}!")\n...\n>>> watch(lambda: a["foo"], callback=my_callback)\n<observ.Watcher object at 0x00000190DAA7EB70>\n>>> a["foo"] = 6\n5 became 6!\n>>>\n>>> @computed\n... def my_computed_property():\n...     print("running")\n...     return 5 * a["foo"]\n...\n>>> assert my_computed_property() == 30\nrunning\n>>> assert my_computed_property() == 30\n>>>\n>>> a["foo"] = 7\n6 became 7!\n>>> assert my_computed_property() == 35\nrunning\n>>> assert my_computed_property() == 35\n>>>\n>>> @computed                                \n... def second_computed_property():          \n...     print("running")                     \n...     return 5 * my_computed_property()    \n...                                          \n>>> assert second_computed_property() == 175 \nrunning                                      \nrunning                                      \n>>> assert second_computed_property() == 175 \n>>>\n>>> a["foo"] = 8                             \n7 became 8!                                  \n>>> assert second_computed_property() == 200 \nrunning                                      \nrunning                                      \n>>> assert second_computed_property() == 200 \n```\n',
    'author': 'Korijn van Golen',
    'author_email': 'korijn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Korijn/observ',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
