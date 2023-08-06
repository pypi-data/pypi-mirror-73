# MuDoPy

MuDoPy is a Python library for downloading songs.

Syntext to download song

import mudopy
mudopy.set_path("path to chromedriver/chromedriver.exe") #Only for the first time enter this line
mudopy("song name","artist name(optional)","Download path(optional)")
#if you not enter download path then library will downloaded into cwd


## Installation

```bash
pip install mudopy
```

## Usage

```python
import mudopy
mudopy.download("Song name",path = None,Artist = None)#Will download the song in cwd


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)