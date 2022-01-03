import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import rasterio
from rasterio.crs import CRS
from rasterio.warp import transform_bounds
from shapely.geometry import box, mapping

JsonDict = Dict[str, Any]


class ImageMetadata:
    def __init__(self, href):
        self.href = href
        self.path = Path(href)
        with rasterio.open(href) as ds:
            self.crs = ds.crs
            self.transform = ds.transform
            self.shape = ds.shape
            self.gsd_x, self.gsd_y = ds.res
            self.bbox = list(ds.bounds)

    @property
    def id(self) -> str:
        return self.path.stem

    @property
    def time_utc(self) -> datetime:
        # Time must be in UTC
        yyyymmdd = re.findall(r'\d+', self.id)[0]
        time_utc = datetime.strptime(yyyymmdd, '%Y%m%d')
        # Timezone of data in filename is unknown in reality
        time_utc = datetime(time_utc.year,
                            time_utc.month,
                            time_utc.day,
                            tzinfo=timezone.utc)
        return time_utc

    @property
    def epsg(self) -> int:
        if self.crs.to_epsg() is not None:
            return self.crs.to_epsg()
        else:
            raise ValueError('Unable to generate EPSG code')

    @property
    def gsd(self) -> float:
        if math.isclose(self.gsd_x, self.gsd_y, abs_tol=0.0001):
            return self.gsd_x
        else:
            raise ValueError('X and Y ground sample distances do not match')

    @property
    def footprint(self) -> JsonDict:
        return mapping(box(*self.bbox))

    @property
    def bbox_wgs84(self) -> List:
        # See also rasterio.warp.transform_geom and rasterio.warp.transform
        dst_crs = CRS.from_epsg(4326)
        bbox_wgs84 = list(transform_bounds(self.crs, dst_crs, *self.bbox))
        return (bbox_wgs84)

    @property
    def footprint_wgs84(self) -> JsonDict:
        footprint_wgs84 = mapping(box(*self.bbox_wgs84))
        return footprint_wgs84
