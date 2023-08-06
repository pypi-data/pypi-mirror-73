from lingua.extractors import Extractor
from lingua.extractors import Message
from yaml.composer import Composer
import sys
import yaml


class YafowilYamlExtractor(Extractor):
    extensions = ['.yaml', '.yml']

    def __call__(self, filename, options):
        self.filename = filename
        self.messages = list()
        self.walk(filename)
        return self.messages

    def walk(self, filename):
        with open(filename) as file:
            loader = yaml.Loader(file.read())

        def compose_node(parent, index):
            node = Composer.compose_node(loader, parent, index)
            self.parse_message(node, loader.line)
            return node
        loader.compose_node = compose_node
        loader.get_single_data()

    def parse_message(self, node, lineno):
        value = node.value
        if not isinstance(value, str):
            return
        if value.startswith('i18n:'):
            parts = value.split(":")
            if len(parts) > 3:
                msg = 'to many : in {0}'.format(value)
                sys.stderr.write(msg)
                return
            if len(parts) == 2:
                message = Message(
                    None, parts[1], None, [], u'', u'',
                    (self.filename, lineno),
                )
            else:
                message = Message(
                    None, parts[1], None, [], u'Default: ' + parts[2], u'',
                    (self.filename, lineno),
                )
            self.messages.append(message)
