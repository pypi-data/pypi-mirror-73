from yafowil.lingua.extractor import YafowilYamlExtractor
import os
import shutil
import tempfile
import unittest


raw = """
factory: form
name: demoform
props:
    action: demoaction
widgets:
- first_field:
    factory: text
    props:
        label: i18n:First Field
- second_field:
    factory: text
    props:
        label: i18n:second_field:Second Field
"""


def temporary_directory(fn):
    def wrapper(inst):
        tempdir = tempfile.mkdtemp()
        try:
            fn(inst, tempdir)
        finally:
            shutil.rmtree(tempdir)
    return wrapper


class TestYafowilLingua(unittest.TestCase):

    @temporary_directory
    def test_extractor(self, tempdir):
        template_path = os.path.join(tempdir, 'tmpl.yaml')
        with open(template_path, 'w') as file:
            file.write(raw)
        extractor = YafowilYamlExtractor()
        res = extractor(template_path, None)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].msgid, 'First Field')
        self.assertEqual(res[0].comment, '')
        self.assertEqual(res[1].msgid, 'second_field')
        self.assertEqual(res[1].comment, 'Default: Second Field')


if __name__ == '__main__':
    unittest.main()
