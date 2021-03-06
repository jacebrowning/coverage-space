# The Coverage Space

> A place to track your code coverage metrics.



[![Test Status](https://img.shields.io/circleci/project/github/jacebrowning/coverage-space/main.svg?label=tests)](https://circleci.com/gh/jacebrowning/coverage-space)
[![Docs Status](https://img.shields.io/travis/jacebrowning/coverage-space/main?label=docs)](https://travis-ci.org/github/jacebrowning/coverage-space)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/coverage-space/main.svg)](https://coveralls.io/r/jacebrowning/coverage-space)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/coverage-space.svg)](https://scrutinizer-ci.com/g/jacebrowning/coverage-space/?branch=main)
[![GitHub Sponsor](https://img.shields.io/badge/server%20costs-%247%2Fmonth-red)](https://github.com/sponsors/jacebrowning)

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
