# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['java_manifest']
setup_kwargs = {
    'name': 'java-manifest',
    'version': '0.1.0',
    'description': "Encode/decode Java's META-INF/MANIFEST.MF in Python",
    'long_description': '# java-manifest-py\n\n[![Build Status](https://travis-ci.com/elihunter173/java-manifest-py.svg?branch=master)](https://travis-ci.com/elihunter173/java-manifest-py)\n\nEncode/decode Java\'s `META-INF/MANIFEST.MF` in Python.\n\n## Installation\n\nTo install the latest release on PyPI, run:\n\n```sh\n$ pip install java-manifest\n```\n\n## Usage\n\nA MANIFEST is represented by a list of dictionaries, where each dictionary\ncorresponds to an empty-line delimited section of the MANIFEST and each\ndictionary has `str` keys and either `str` or `bool` values.\n\n`java_manifest.loads` takes a string containing MANIFEST-formatted data and\nreturns a list of dictionaries, where each dictionary is a section in the\nMANIFEST. `java_manifest.load` does the same, using any `typing.TextIO`\nreadable object.\n\n```python\n>>> import java_manifest\n>>> manifest_str = """\n... Name: README-Example-1\n... Boolean: true\n... Long-Line: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n...  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n...\n... Name: README-Example-2\n... Boolean: false\n... Not-Boolean: False\n... """\n>>> manifest = java_manifest.loads(manifest_str)\n>>> print(parsed_manifest)\n[{\'Name\': \'README-Example-1\', \'Boolean\': True, \'Long-Line\': \'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\'}, {\'Name\': \'README-Example-2\', \'Boolean\': False, \'Not-Boolean\': \'False\'}]\n```\n\nSimilarly, `java_manifest.dumps` returns a string of MANIFEST-formatted data\nfrom a list of dictionaries, where each dictionary is a section in the\nMANIFEST. `java_manifest.dump` does the same, writing into any `typing.TextIO`\nwritable object.\n\n```python\n>>> import java_manifest\n>>> manifest = [\n...     {\n...         "Name": "README-Example",\n...         "Some-Str": "Some random string",\n...         "Some-Bool": True,\n...     },\n... ]\n>>> manifest_str = java_manifest.dumps(manifest)\n>>> print(manifest_str)\nName: README-Example\nSome-Str: Some random string\nSome-Bool: true\n\n```\n\nThere is also a `from_jar` function that finds the `META-INF/MANIFEST.MF` file\nwithin the jar and `java_manifest.load`s that.\n\n```python\n>>> import java_manifest\n>>> manifest = java_manifest.from_jar("/path/to/jarfile.jar")\n```\n',
    'author': 'Eli W. Hunter',
    'author_email': 'elihunter173@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/elihunter173/java-manifest-py',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
