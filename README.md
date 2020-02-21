# Samitizer

[![Actions Status](https://github.com/theeluwin/samitizer/workflows/build/badge.svg)](https://github.com/theeluwin/samitizer/actions)
[![Coverage Status](https://coveralls.io/repos/github/theeluwin/samitizer/badge.svg?branch=master)](https://coveralls.io/github/theeluwin/samitizer?branch=master)
[![PyPI version](https://badge.fury.io/py/samitizer.svg)](https://badge.fury.io/py/samitizer)

A Python library for parsing SAMI files.

This project was once [theeluwin/PySAMI](https://github.com/theeluwin/PySAMI), which was forked from [g6123/PySAMI](https://github.com/g6123/PySAMI), thus the license is preserved as @g6123's.


## Installation

```bash
$ pip install samitizer
```

To use the automatic charset detection feature, you need to install the `uchardet` too.

```bash
$ sudo apt-get install uchardet
```

## Usage


```python
from samitizer import Sami

# Using `encoding=None` will invoke the `uchardet` with a subprocess call.
# Tip: try `encoding='cp949'` if nothing works.
sami = Sami('sample.smi', encoding=None)

# These `subtitles` are intances of the `samitizer.Subtitle` class.
print(sami.subtitles[0].lang2content['KRCC'])

vtt_text = sami.convert('vtt', lang='KRCC')
plain_text = sami.convert('plain', lang='KRCC')
```

## Test

Testing requires some additional packages (`flake8` is optional though).

```bash
$ pip install nose nose-exclude flake8 coverage
```

You can test with the [nose](https://nose.readthedocs.io/)

```bash
$ nosetests --config=.noserc
```

or, with docker.

```bash
$ docker build -t samitizer -f Dockerfile .
$ docker run samitizer
```
