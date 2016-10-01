# The Coverage Space

> A place to track your code coverage metrics.

[![Build Status](http://img.shields.io/travis/jacebrowning/coverage-space/master.svg)](https://travis-ci.org/jacebrowning/coverage-space)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/coverage-space/master.svg)](https://coveralls.io/r/jacebrowning/coverage-space)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/coverage-space.svg)](https://scrutinizer-ci.com/g/jacebrowning/coverage-space/?branch=master)

## Quick Start

### Prerequisites

The API can be used with `curl`, but [HTTPie](https://github.com/jkbrzt/httpie) is preferred:

```sh
$ pip install HTTPie
```

### Commands

Get the latest coverage metrics:

```sh
$ http GET api.coverage.space/my_owner/my_repo
```

Update coverage metrics:

```sh
$ http PUT api.coverage.space/my_owner/my_repo unit=90 --check-status
```

Reset coverage metrics:

```sh
$ http DELETE api.coverage.space/my_owner/my_repo
```

## Documentation

Read the full docs at [coverage.space](https://coverage.space).
