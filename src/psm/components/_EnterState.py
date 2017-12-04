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

from psm import EventRecordable


class EnterState(EventRecordable):
    def __init__(self, logid, name, data, timestamp=None):
        self.logid = logid
        self.name = name
        self.timestamp = timestamp
        self.data = data

    @classmethod
    def recoverSpecific(cls, event):
        "For all EnterState's subclasses' recovery form log"
        return cls(event.event_id, event.event_name, event.data, event.timestamp)

    def _log(self, logger):
        "Log state is already handled by PyTransition when generating PSM"
        pass

    @classmethod
    def logInit(cls, logger):
        empty_data_func = lambda: {}
        logger.logEnterState(empty_data_func, None, name='Init')

    def aggregate_data(self, aggregated_data):
        if not self.data:
            return
        for key in self.data:
            aggregated_data[key] = self.data[key]
