import unittest

from stactools.aerial import stac
from tests import test_data


class StacTest(unittest.TestCase):

    def test_create_collection(self):
        collection = stac.create_collection()
        collection.set_self_href("")

        self.assertEqual(collection.id, "test-aerial-imagery")
        self.assertEqual(collection.extent.spatial.to_dict()["bbox"],
                         [[-180., 90., 180., -90.]])

        collection.validate()

    def test_create_item(self):
        path = test_data.get_external_data("UFO_USACE_EO_20190308.1618_11.tif")
        item = stac.create_item(path)

        self.assertEqual(item.id, "UFO_USACE_EO_20190308.1618_11")

        item.validate()
