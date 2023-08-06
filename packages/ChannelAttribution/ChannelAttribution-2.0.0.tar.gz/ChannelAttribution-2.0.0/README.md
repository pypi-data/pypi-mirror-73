Python library *ChannelAttribution*
===================================

Installation
------------

### From PyPi

```bash
pip install --upgrade setuptools
pip install ChannelAttribution
```


Generating distribution archives
--------------------------------

```bash
python setup.py sdist bdist_wheel
```

Generating documentation
------------------------

```bash
pip install Sphinx
pip install rinohtype

cd /src/cypack
python generate_doc.py
```

Documentation will be generate at \src\cypack\docs\_build
