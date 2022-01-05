# stactools-aerial

- Name: aerial
- Package: `stactools.aerial`
- Owner: pjhartzell
- Dataset homepage: https://github.com/pjhartzell/aerial
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [eo](https://github.com/stac-extensions/eo)

Toy stactools package to create STAC items and collections for select airborne imagery.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pjhartzell/aerial/main?filepath=docs/installation_and_basic_usage.ipynb)

## Examples

### STAC objects

- [Collection](examples/collection.json)
- [Item](examples/EO_20190308.1618_11/EO_20190308.1618_11.json)

### Command-line usage

Create an empty collection.

```bash
$ stac aerial create-collection collection.json
```

Create a single item.

```bash
$ stac aerial create-item aerial_image.tif item.json
```

Use `stac aerial --help` to see all subcommands and options.

### Python usage

Use within a Python script to create an empty collection, add items to the collection, update and save the (now no longer empty) collection.

```python
from pathlib import Path

from pystac.catalog import CatalogType
from stactools.aerial import create_collection, create_item

# Path to aerial TIF files
DATA_PATH = '/Users/pjh/data/aerial/'

# Create an empty collection
collection = create_collection()

# Add items to the collection
files = list(Path(DATA_PATH).glob('*.tif'))
for file in files:
    print(f'creating STAC item for {file.name}')
    item = create_item(str(file))
    collection.add_item(item)

# Update the collection extent based on the added items
collection.update_extent_from_items()

# Normalize hrefs
stac_path = str(Path(DATA_PATH) / 'STAC')
collection.normalize_hrefs(stac_path)

# Save the collection
collection.save(catalog_type=CatalogType.SELF_CONTAINED)
print(f'STAC written to {stac_path}')
```
