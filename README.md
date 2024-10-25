## Commands

```sh
# Run
uv run -m printer_keeper

# Continuous testing
uv run ptw .
uv run ptw . -m "not annoying" --snapshot-update
uv run ptw . -m "not annoying" --maxfail=1 -vvv
```

GitHub Actions

```sh
# Run GitHub workflow locally
act push
```
