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

import copy

from psm import EventRecordable

class Trigger(EventRecordable):
    """ Trigger serves as the entry point for a psm's generation and state recovery.
        Also, trigger holds all the data inputs to the psm from the outside world!
    """
    fields = {}
    _psm_data_prefix = ""

    def __init__(self, logid=None, name=None, data={}, timestamp=None):
        self.logid = logid
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__
        self.data = data
        self.timestamp = timestamp

    @classmethod
    def recoverSpecific(cls, event):
        "For all Trigger's subclasses' recovery from log"
        trigger = cls(event.event_id, event.event_name, event.data, event.timestamp)
        trigger.regularize()
        return trigger

    def log(self, logger):
        logger.logTrigger(self.__class__.__name__, self.data)

    def store(self, data):
        self.data = data
        self.regularize()

    def aggregate_data(self, aggregated_data):
        if not self.data:
            return
        prefix = self._psm_data_prefix
        if prefix not in aggregated_data:
            if prefix == 'trainingloss':
                aggregated_data[prefix] = []
            else:
                aggregated_data[prefix] = {}
        if prefix == 'trainingloss':
            aggregated_data[prefix].append(self.data)
        else:
            aggregated_data[prefix] = {**self.data, **aggregated_data[prefix]}

    def regularize(self):
        result = copy.deepcopy(self.data)
        for field in self.fields:
            if field not in self.data:
                raise AttributeError('Required field <{}> not found'.format(field))
            result[field] = self.fields[field](self.data[field])
        self.data = result
