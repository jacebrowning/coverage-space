# RESTful API

The API is available at [https://api.coverage.space](https://api.coverage.space). When viewed in a browser, an HTML interface is displayed. For an example, check out [https://api.coverage.space/my_owner/my_repo](https://api.coverage.space/my_owner/my_repo).

The API is also accessible from the command-line. The following examples will use [HTTPie](https://github.com/jkbrzt/httpie) for simplicity, but the same could be accomplished with `curl`. To install the HTTP client:

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
$ http DELETE api.coverage.space/my_owner/my_repo
```

or specify a particular branch:

```sh
$ http DELETE api.coverage.space/my_owner/my_repo/my_branch
```
