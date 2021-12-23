from pathlib import Path

from pystac.catalog import CatalogType

from stac import create_collection, create_item


DATA_PATH = '/Users/pjh/data/aerial/'

collection = create_collection()

files = list(Path(DATA_PATH).glob('*.tif'))
for file in files:
    print(f'creating STAC item for {file.name}')
    item = create_item(str(file))
    collection.add_item(item)

collection.update_extent_from_items()

# Normalize hrefs
stac_path = str(Path(DATA_PATH) / 'STAC')
collection.normalize_hrefs(stac_path)

# Save the collection
collection.save(catalog_type=CatalogType.SELF_CONTAINED)
print(f'STAC written to {stac_path}')