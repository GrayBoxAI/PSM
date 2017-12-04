#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Unit tests for MockLogger."""
import unittest

from ._mock import MockLogger


class TestMockLogger(unittest.TestCase):
    def setUp(self):
        self.logger = MockLogger()

    def test_bad_input(self):
        typ = 'NotEnterState'
        name = 'someName'
        with self.assertRaises(TypeError):
            self.logger.logAnyEvent(typ, name)

    def test_(self):
        pass
