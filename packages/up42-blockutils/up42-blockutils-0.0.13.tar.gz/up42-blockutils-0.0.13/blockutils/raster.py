"""
Common raster handling methods shared between blocks
"""
from pathlib import Path

import numpy as np
import rasterio as rio


def is_empty(path_to_image: Path, nodataval=0) -> bool:
    """
    Tests if a created geotiff image only consists of nodata or NaN values
    Converts NaN to nodata values as a side effect
    Args:
        path_to_image: Path object pointing to geotiff image
        nodataval: no data value, default is 0

    Returns: True if image is empty, False otherwise
    """
    with rio.open(str(path_to_image)) as img_file:
        data = img_file.read()
        np.nan_to_num(data, nan=nodataval, copy=False)
        return not np.any(data - nodataval)
