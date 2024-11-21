
# `mimetypeplus`

> A simple python module focused on easy MIME type manipulation and detection.

[![CodeQL](https://github.com/MarkusHammer/mimetypeplus-python/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/MarkusHammer/mimetypeplus-python/actions/workflows/github-code-scanning/codeql) [![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/markushammer)

[Documentation](https://MarkusHammer.github.io/mimetypeplus-python)

## Setup

This module can be installed using:

```bash
pip install mimetypeplus
```

## Usage

This module is intended to be used only as a module, and can be imported after installing using the traditional process:

```python
from mimetypeplus import MimeType
```

### Create a MIME Type Object

```python
mime = MimeType("application/json")
```

### Identify MIME Types

Quickly determine the MIME type of content from various sources:

```python
# Identify MIME type from a file path
mime = MimeType.from_path("data.json")
mime = MimeType.from_path(__file__)

# Identify MIME type from a URI
mime = MimeType.from_uri("https://example.com/api/data")
```

### Facet Manipulation

```python
# Check if the MIME type is experimental
if mime.experimental_facet:
    print("This is an experimental MIME type.")

# Set a vendor-specific facet
mime.facet = "vnd"
```

### Quickly Find File Extensions

```python
extension = mime.to_extention()
print(f"The file extension for this MIME type is '{extension}'")
```

### And More

There are a handfull of other ease of use features that this module provides, feel free to reference the [documentation](https://MarkusHammer.github.io/mimetypeplus-python) for more information.

## Licence

This is licensed under the Mozilla Public License 2.0 (MPL 2.0) Licence. See the Licence file in this repository for more information.

## Contribute

Contributions are always welcome!
Use the [github repository](https://github.com/MarkusHammer/mimetypeplus-python) to report issues and contribute to this project.

## Credits

While not required, feel free to credit "Markus Hammer" (or just "Markus") if you find this code or script useful for whatever you may be doing with it.
