# This file exists within 'nark':
#
#   https://github.com/tallybark/nark
#
# Copyright © 2018-2020 Landon Bouma
# Copyright © 2015-2016 Eric Goller
# All  rights  reserved.
#
# 'nark' is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License  as  published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any   later    version.
#
# 'nark' is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY  or  FITNESS FOR A PARTICULAR
# PURPOSE.  See  the  GNU General Public License  for  more details.
#
# You can find the GNU General Public License reprinted in the file titled 'LICENSE',
# or visit <http://www.gnu.org/licenses/>.

"""Base fixtures available to all nark tests."""

import pytest

from nark.control import NarkControl
from nark.manager import BaseStore

# (lb): I moved lots of conftest functions to nark.tests so that downstream
#   packages can reuse the same fixtures. However, it's uncouth to `import *`,
#   so the linter lets us have it. But conftest.py is already magic -- pytest
#   loads conftest for every test_xxx.py file -- so it's already akin to being
#   *-glob imported. Which is what we do here, linter and best practices be
#   damned. Furthermore, the pytest-factoryboy register() functions also
#   magically injects fixtures into the namespace (that themselves are mutated
#   from a corresponding classname, e.g., FactFactory becomes a fixture named
#   fact_factory). So I don't know what all the fuss is about, just import *.
# F401 'nark.tests.conftest.*' imported but unused
# F403 'from nark.tests.conftest import *' used; unable to detect undefined names
from nark.tests.conftest import *  # noqa: F401, F403


@pytest.yield_fixture
def controller(base_config):
    """Provide a basic controller."""
    # From hamster-lib: "[TODO] Parametrize over all available stores."
    # (lb): And yet in dob there's still just the one for SQLite.
    controller = NarkControl(base_config)
    yield controller
    controller.store.cleanup()


@pytest.fixture
def basestore(base_config):
    """Provide a generic ``storage.BaseStore`` instance using ``baseconfig``."""
    store = BaseStore(base_config)
    return store

