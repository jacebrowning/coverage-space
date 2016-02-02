# The Coverage Space

> ...a place to track your code coverage metrics.

The examples will use [HTTPie](https://github.com/jkbrzt/httpie) for simplicity, but the same could be accomplished with `curl`. To install it:

```sh
$ pip install HTTPie
```

## Getting Metrics

To get the latest coverage metrics:

```sh
$ http GET api.coverage.space/my_owner/my_repo
```

or specify a particular branch:

```sh
$ http GET api.coverage.space/my_owner/my_repo/my_branch
```

## Updating Metrics

To update coverage metrics:

```sh
$ http PUT api.coverage.space/my_owner/my_repo unit=90 --check-status
```

or specify a particular branch:

```sh
$ http PUT api.coverage.space/my_owner/my_repo/my_branch unit=90 --check-status
```

## Reseting Metrics

To reset the coverage metrics:

```sh
$ http POST api.coverage.space/my_owner/my_repo/reset
```

or specify a particular branch:

```sh
$ http POST api.coverage.space/my_owner/my_repo/my_branch/reset
```
