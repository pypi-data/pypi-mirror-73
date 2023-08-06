"""vartoml - Enable variables in a TOML file"""

__version__ = '0.9.5'
__author__ = 'Manfred Lotz <manfred.lotz@posteo.de>'
# __all__ = []

import toml
import os
import re

from typing import List, Dict, Match, Any, MutableMapping


"""
According to the TOML specification (https://toml.io/en/v1.0.0-rc.1)

- naming rules for sections (aka tables) are the same as for keys
- keys may consist of ASCII letters, digits, underscores and dashes


Example:

database = "/var/db/mydb.db"
home_dir = "/home/johndoe"
db-port = 4711
_a = "hey"
-bla = "something"
1ab = true

"""
RE_VAR = re.compile(r"""
             [$][{]
             (
                [a-zA-Z0-9_-]+     # section name
                ([:][a-zA-Z0-9_-]+)+     # variable name
             )
             [}]
""", re.VERBOSE)

class VarToml:
    def __init__(self) -> None:
        self.decoder = toml.TomlDecoder()

    def load(self, *args, **kwargs):
        self.data = toml.load(*args, **kwargs)
        self._process(self.data)

    def loads(self, *args, **kwargs):
        self.data = toml.loads(*args, **kwargs)
        self._process(self.data)

    def _var_replace(self, x):
        toml_var = x.groups()[0]
        lst = toml_var.split(':')
        val = self.data[lst[0]]
        for v in lst[1:]:
            val = val[v]

        return str(val)

    def get(self, *args):
        gotten = self.data
        for arg in args:
            gotten = gotten[arg]
        return gotten

    def dict(self):
        return self.data

    def _process(self, item):
        iter_ = None
        if isinstance(item, dict):
            iter_ = item.items()
        elif isinstance(item, list):
            iter_ = enumerate(item)

        for i, val in iter_:
            if isinstance(val, (dict, list)):
                self._process(val)
            elif isinstance(val, str):
                if re.search(RE_VAR, val):
                    r = re.sub(RE_VAR, self._var_replace, val)

                    # Try to first load the value from the variable contents
                    # (i.e. make what seems like a float a float, what seems like a
                    # boolean a bool and so on). If that fails, fail back to
                    # string.
                    try:
                        item[i], _ = self.decoder.load_value(r)
                        continue
                    except ValueError:
                        pass

                    item[i], _ = self.decoder.load_value('"{}"'.format(r))
