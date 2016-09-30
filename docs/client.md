# Command-line Client

To automate the process of updating coverage metrics, the official command-line client can be used to interact with the API:

```sh
pip install --upgrade coverage.space
```

## Updating Metrics

To update coverage metrics:

```sh
coverage.space <slug> <metric>
```

where:

- slug = project URL path (e.g. `my_owner/my_repo`)
- metric = coverage metric to update (i.e. `unit`, `integration`, or `overall`)

## Additional Reading

For additional options and supported coverage formats, see the [full documentation](https://cli.coverage.space).
