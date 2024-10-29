## Commands

```sh
# Run
uv run -m printer_keeper

# Continuous testing
uv run ptw .
uv run ptw . -m "not annoying" --snapshot-update
uv run ptw . --maxfail=1 -vvv
```

### Printer not printing

```
lpstat -p
```

Might say something like

```
printer Canon_G6000_series disabled since Sat Oct 26 07:55:01 2024 -
        Unable to add document to print job.
```

Fix it with

```
cupsenable Canon_G6000_series
```

## GitHub Actions

Test GitHub workflow locally

```sh
act push
```
