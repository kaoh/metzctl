# Summary

Metz television remote onctrol library

# Usage

~~~
rom metzctl import Remote
from metzctl.remote import TvRemoteCommandException

remote = Remote("192.168.178.44", debug=True)
remote.volume_up()
~~~

# Development

## Local Installation

    pip install
    
will take the `setup.py` and install it.

## Increment Version

Requirement:
 
~~~
pip install bumpversion
~~~

Minor increment:

~~~
bumpversion --current-version 1.0.0 minor setup.py metzctl/__init__.py
~~~

Major increment:

~~~
bumpversion --current-version 1.1.9 major setup.py metzctl/__init__.py
~~~

## Deploy

~~~
pip install twine
~~~

To create a source archive and a wheel for your package:

~~~
python setup.py sdist bdist_wheel
~~~

~~~
cd dist
tar tzf metzctl....tar.gz
twine check dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
~~~

Publish it to PyPI:

~~~
twine upload dist/*
~~~
