from datetime import datetime, timezone

from pystac import (Asset, CatalogType, Collection, Extent, Item, MediaType,
                    SpatialExtent, TemporalExtent)
from pystac.extensions.eo import Band, EOExtension
from pystac.extensions.projection import ProjectionExtension

from stactools.aerial.constants import PROVIDERS
from stactools.aerial.image_metadata import ImageMetadata


def create_collection() -> Collection:
    """Create a STAC Collection

    See `Collection<https://pystac.readthedocs.io/en/latest/api.html#collection>`_.

    Returns:
        Collection: STAC Collection object
    """

    collection_id = 'test-aerial-imagery'
    collection_title = 'aerial images'
    collection_description = 'Preston\'s test collection of aerial images'

    # Time must be in UTC
    time = datetime.now(tz=timezone.utc)
    extent = Extent(
        SpatialExtent([[-180., 90., 180., -90.]]),
        TemporalExtent([time, None]),
    )

    collection = Collection(
        id=collection_id,
        title=collection_title,
        description=collection_description,
        license='proprietary',
        providers=PROVIDERS,
        extent=extent,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
    )

    return collection


def create_item(asset_href: str) -> Item:
    """Create a STAC Item

    See `Item<https://pystac.readthedocs.io/en/latest/api.html#item>`_.

    Args:
        asset_href (str): The HREF pointing to an asset associated with the item

    Returns:
        Item: STAC Item object
    """

    # metadata class instance
    image_metadata = ImageMetadata(asset_href)

    # item instance
    item = Item(
        id=image_metadata.id,
        geometry=image_metadata.footprint_wgs84,
        bbox=image_metadata.bbox_wgs84,
        datetime=image_metadata.time_utc,
        properties={}
    )

    # --Common Metadata--
    item.common_metadata.gsd = image_metadata.gsd
    item.common_metadata.providers = PROVIDERS
    item.common_metadata.license = 'proprietary'

    # --Extensions--
    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.epsg = image_metadata.epsg
    projection.transform = image_metadata.transform[0:6]
    projection.shape = image_metadata.shape
    projection.bbox = image_metadata.bbox
    projection.geometry = image_metadata.footprint

    # --Assets--
    asset = create_image_asset(asset_href, item)
    item.add_asset('image', asset)

    item.validate()

    return item


def create_image_asset(href: str, item: Item) -> Asset:
    asset = Asset(href=href,
                  media_type=MediaType.GEOTIFF,
                  roles=['data'])
    item.add_asset(key='image', asset=asset)

    # --Extensions--
    eo = EOExtension.ext(asset, add_if_missing=True)
    rgb_bands = [Band.create(name='1', common_name='red'),
                 Band.create(name='2', common_name='green'),
                 Band.create(name='3', common_name='blue')]
    eo.bands = rgb_bands

    return asset
