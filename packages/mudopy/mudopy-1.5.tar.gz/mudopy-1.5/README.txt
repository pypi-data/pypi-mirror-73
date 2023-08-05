# MuDoPy

MuDoPy is a Python library for downloading songs.

## Installation

```bash
pip install mudopy
```

## Usage

```python
import mudopy
mudopy.set_path("Path to chromedriver") #You must call this for the first time
mudopy.download("Song name",path = None,Artist = None)#Will download the song in cwd


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)