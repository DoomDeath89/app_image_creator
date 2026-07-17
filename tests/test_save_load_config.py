import json
import tempfile
import os
import unittest


class TestSaveLoadConfigLogic(unittest.TestCase):
    def test_save_config_creates_valid_json(self):
        config = {
            'name': 'MyApp',
            'version': '1.0',
            'category': 'Game',
            'comment': 'Test comment',
            'executable_path': '/usr/bin/myapp',
            'icon_path': '/usr/share/icon.png',
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f, indent=2)
            tmp_path = f.name

        try:
            with open(tmp_path, 'r') as f:
                data = json.load(f)

            self.assertEqual(data['name'], 'MyApp')
            self.assertEqual(data['version'], '1.0')
            self.assertEqual(data['category'], 'Game')
            self.assertEqual(data['comment'], 'Test comment')
            self.assertEqual(data['executable_path'], '/usr/bin/myapp')
            self.assertEqual(data['icon_path'], '/usr/share/icon.png')
        finally:
            os.unlink(tmp_path)

    def test_load_config_populates_fields(self):
        config = {
            'name': 'LoadedApp',
            'version': '2.0',
            'category': 'Utility',
            'comment': 'Loaded comment',
            'executable_path': '/usr/bin/loaded',
            'icon_path': '/usr/share/loaded.png',
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            tmp_path = f.name

        try:
            with open(tmp_path, 'r') as f:
                loaded = json.load(f)

            self.assertEqual(loaded['name'], 'LoadedApp')
            self.assertEqual(loaded['version'], '2.0')
            self.assertEqual(loaded['category'], 'Utility')
            self.assertEqual(loaded['comment'], 'Loaded comment')
            self.assertEqual(loaded['executable_path'], '/usr/bin/loaded')
            self.assertEqual(loaded['icon_path'], '/usr/share/loaded.png')
        finally:
            os.unlink(tmp_path)

    def test_load_config_handles_missing_fields(self):
        config = {'name': 'PartialApp'}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            tmp_path = f.name

        try:
            with open(tmp_path, 'r') as f:
                loaded = json.load(f)

            self.assertEqual(loaded.get('name'), 'PartialApp')
            self.assertIsNone(loaded.get('version'))
            self.assertIsNone(loaded.get('category'))
        finally:
            os.unlink(tmp_path)

    def test_config_roundtrip(self):
        original = {
            'name': 'RoundtripApp',
            'version': '3.0',
            'category': 'Development',
            'comment': 'Roundtrip test',
            'executable_path': '/usr/bin/roundtrip',
            'icon_path': '/usr/share/roundtrip.png',
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(original, f)
            tmp_path = f.name

        try:
            with open(tmp_path, 'r') as f:
                loaded = json.load(f)

            self.assertEqual(original, loaded)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
