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

from datetime import datetime

from ._base import PersistentEventLogger

class MockLogger(PersistentEventLogger):
    def __init__(self):
        self.if_mock = True
        self._mocklogger = []
        self.curr_id = 0

    def records(self):
        "return a generator to the log"
        return self._mocklogger

    def empty(self):
        if self.if_mock:
            return not self._mocklogger
        else:
            raise NotImplementedError

    def _log_event_dic(self, dic):
        self._mocklogger.append(dic)

    def printmocklog(self):
        for idx, record in enumerate(self._mocklogger):
            print(idx)
            print(record)
            print()
