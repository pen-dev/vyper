import io
import json
import unittest
from builtins import str as text

import toml
import vyper
import yaml


yaml_example = '''Hacker: true
name: steve
hobbies:
- skateboarding
- snowboarding
- go
clothing:
  jacket: leather
  trousers: denim
  pants:
    size: large
age: 35
eyes : brown
beard: true'''

toml_example = 'title = "TOML Example"\n' \
               '[owner]\n' \
               'organization = "MongoDB"\n' \
               'Bio = "MongoDB Chief Developer Advocate & Hacker at Large"\n' \
               'dob = 1979-05-27T07:32:00Z # First class dates? Why not?'

json_example = {
    "id": "0001",
    "type": "donut",
    "name": "Cake",
    "ppu": 0.55,
    "batters": {
        "batter": [
            {"type": "Regular"},
            {"type": "Chocolate"},
            {"type": "Blueberry"},
            {"type": "Devil's Food"}
        ]
    }
}


class TestVyper(unittest.TestCase):
    def setUp(self):
        self.v = vyper.Vyper()

    def _init_configs(self):
        self.v.set_config_type('yaml')
        r = yaml.dump(text(yaml_example))
        self.v._unmarshall_reader(r, self.v.config)

        self.v.set_config_type('json')
        r = io.StringIO(text(json.dumps(json_example)))
        self.v._unmarshall_reader(r, self.v.config)

        self.v.set_config_type('toml')
        r = toml.loads(toml_example)
        self.v._unmarshall_reader(r, self.v.config)

    def _init_yaml(self):
        self.v.set_config_type('yaml')
        r = yaml.dump(text(yaml_example))
        self.v._unmarshall_reader(r, self.v.config)

    def _init_json(self):
        self.v.set_config_type('json')
        r = io.StringIO(text(json.dumps(json_example)))
        self.v._unmarshall_reader(r, self.v.config)

    def _init_toml(self):
        self.v.set_config_type('toml')
        r = toml.loads(toml_example)
        self.v._unmarshall_reader(r, self.v.config)

    # def test_basics(self):
    #    self.v.set_config_file('/tmp/config.yaml')
    #    self.assertEqual('/tmp/config.yaml', self.v._get_config_file())

    def test_default(self):
        self.v.set_default('age', 45)
        self.assertEqual(45, self.v.get('age'))

        self.v.set_default('clothing.jacket', 'slacks')
        self.assertEqual('slacks', self.v.get('clothing.jacket'))

    def test_override(self):
        self.v.set('age', 40)
        self.assertEqual(40, self.v.get('age'))

    def test_default_post(self):
        self.assertNotEqual('NYC', self.v.get('state'))
        self.v.set_default('state', 'NYC')
        self.assertEqual('NYC', self.v.get('state'))

    def test_aliases(self):
        self.v.register_alias('years', 'age')
        self.v.set('years', 45)
        self.assertEqual(45, self.v.get('age'))

    def test_yaml(self):
        self._init_yaml()
        self.assertEqual('steve', self.v.get('name'))

    def test_json(self):
        self._init_json()
        self.assertEqual('0001', self.v.get('id'))

    def test_toml(self):
        self._init_toml()
        self.assertEqual('TOML Example', self.v.get('title'))

    def test_case_insensitive(self):
        self.v.set('Title', 'Checking Case')
        self.assertEqual('Checking Case', self.v.get('tItle'))

    def test_aliases_of_aliases(self):
        self.v.register_alias('Foo', 'Bar')
        self.v.register_alias('Bar', 'Title')
        self.v.set('Foo', 'Checking Case')

        self.assertEqual('Checking Case', self.v.get('Bar'))

    def test_recursive_aliases(self):
        self.v.register_alias('Baz', 'Roo')
        self.v.register_alias('Roo', 'baz')