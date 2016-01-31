# The Coverage Space

> ...a place to track your code coverage metrics.

## Updating Metrics

The examples will use [HTTPie](https://github.com/jkbrzt/httpie) for simplicity, but the same could be accomplished with `curl`. To install it:

```sh
$ pip install httpie
```

To update coverage metrics:

```sh
$ http patch api.coverage.space/owner/repo unit=90 --check-status
```
