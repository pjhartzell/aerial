import os.path
from tempfile import TemporaryDirectory

import pystac
from stactools.testing import CliTestCase

from stactools.aerial.commands import create_aerial_command
from tests import test_data


class CommandsTest(CliTestCase):

    def create_subcommand_functions(self):
        return [create_aerial_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            outfile = os.path.join(tmp_dir, "collection.json")
            args = ["aerial", "create-collection", outfile]
            result = self.run_command(args)
            self.assertEqual(result.exit_code, 0)
            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)
            collection = pystac.read_file(outfile)
            self.assertEqual(collection.id, "test-aerial-imagery")
            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:
            infile = test_data.get_external_data(
                "UFO_USACE_EO_20190308.1618_11.tif")
            outfile = os.path.join(tmp_dir, "item.json")
            args = ["aerial", "create-item", infile, outfile]
            result = self.run_command(args)
            self.assertEqual(result.exit_code, 0)
            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)
            item = pystac.read_file(outfile)
            item.validate()
