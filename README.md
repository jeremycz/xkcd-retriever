# XKCD Retriever

A module which uses the [XKCD API](https://xkcd.com/json.html) to display comics.

## Installation

- Tested with Python 3.9.6

```
pip install -r requirements.txt
```

## Command-line Use

```
python3 -m xkcd [-h] [-i INDEX] [-r] [-l]

optional arguments:
  -h, --help                show this help message and exit
  -i INDEX, --index INDEX   display a specific comic by index
  -r, --random              display a random comic
  -l, --latest              display the latest comic
  -n, --nodisplay           suppress comic display
```

Running with no command line arguments will display the index of the most recent comic. This can be used to select an appropriate value to use with the `-i` command line argument.

## Programmatic Use

Import the package.

```python
from xkcd.retriever import Retriever
```

Instantiate an instance of the retriever class.

```python
retriever = Retriever(display_comic: bool = False)
```

Initialise the retriever.

```python
retriever.initialise() -> (success: bool, latest_comic_index: int | None)
```

Display the latest, random or a specific comic. Methods return the comic data in a dict on success, or `None` if unsuccessful.

```python
retriever.get_latest() -> dict | None
retriever.get_random() -> dict | None
retriever.get_comic(ind: int) -> dict | None
```

