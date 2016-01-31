# The Coverage Space

Track code coverage metrics.

[![Build Status](http://img.shields.io/travis/jacebrowning/coverage-space/master.svg)](https://travis-ci.org/jacebrowning/coverage-space)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/coverage-space/master.svg)](https://coveralls.io/r/jacebrowning/coverage-space)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/coverage-space.svg)](https://scrutinizer-ci.com/g/jacebrowning/coverage-space/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/coverage.space.svg)](https://pypi.python.org/pypi/coverage.space)
[![PyPI Downloads](http://img.shields.io/pypi/dm/coverage.space.svg)](https://pypi.python.org/pypi/coverage.space)

## Scripted Interaction

The examples will use [HTTPie](https://github.com/jkbrzt/httpie) for simplicity, but the same could be accomplished with `curl`. To install it:

```sh
$ pip install HTTPie
```

To update coverage metrics:

```sh
$ http patch api.coverage.space/owner/repo unit=90 --check-status
```
