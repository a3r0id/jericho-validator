# jericho-validator
 Validate arbitrary image uploads from incoming data urls while preserving file integrity but removing EXIF and unwanted artifacts and RCE exploit potential.

[![PyPI version](https://badge.fury.io/py/jericho-validator.svg)](https://badge.fury.io/py/jericho-validator)

### Installation
PyPi: `pip install jericho-validator`

Manually: `python setup.py install`

### Example Usage
```python
from requests import get
from jericho_validator import Jericho


example_b64 = "https://raw.githubusercontent.com/hostinfodev/jericho-validator/main/example/example.png.b64"

b64_url = get(example_b64).text

def test_valid_b64(b64_url):    

    try:
        # Check the data URL (image)
        j = Jericho.jericho(b64_url)

    except Jericho.Exceptions.ImageTooLarge:
        print('Image is too large.')

    except Jericho.Exceptions.EmptyFileName:
        print('File name is empty.')
        
    except Jericho.Exceptions.UnsupportedImageType:
        print('Image type not supported.')

    except Exception as e:
        print(e)
        
    if j.isValid:
        print('Image is valid.')
        print('Image size in bytes: ' + str(j.sizeBytes))
        print('Image dimensions: ' + str(j.dimensions))
        print('Image filename: ' + j.filename)
        print('Image extension: ' + j.extension)
        print('Image format prefix: ' + j.formatPrefix)
        
    else:
        print('Image is invalid.')


if __name__ == '__main__':
    test_valid_b64(b64_url)

```