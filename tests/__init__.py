from stactools.testing.test_data import TestData

EXTERNAL_DATA = {
    'UFO_USACE_EO_20190308.1618_11.tif': {
        'url': ('https://pjhartzell.blob.core.windows.net/images/'
                'UFO_USACE_EO_20190308.1618_11.tif'),
        'compress':
        None
    }
}

test_data = TestData(__file__, external_data=EXTERNAL_DATA)
