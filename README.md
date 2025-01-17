# Plot5D

The easiest way to run Plot5D is to use [uv](https://github.com/astral-sh/uv) and Dash directly.

To install `uv` on Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then to run Plot5D

```sh
git clone https://github.com/nplinden/Plot5D.git
cd Plot5D
uv run main.py -f /path/to/csv/file
``` 

By default Plot5D will find an unused port to run on.
You can explicitely set a port using the `-p` argument.



