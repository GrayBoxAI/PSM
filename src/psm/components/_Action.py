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


class Action(EventRecordable):
    fields = {}

    def __init__(self, logid=None, name=None, data={}, timestamp=None):
        self.logid = logid
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__
        self.data = data
        self.timestamp = timestamp
        self.regularize()

    def regularize(self):
        result = copy.deepcopy(self.data)
        for field in self.fields:
            if field not in self.data:
                err_msg = "Required field <{}> not found for action <{}>"
                raise AttributeError(err_msg.format(field, self))
            result[field] = self.fields[field](self.data[field])
        self.data = result

    @classmethod
    def recoverSpecific(cls, event):
        "For all EnterState's subclasses' recovery form log"
        return cls(event.event_id, event.event_name, event.data, event.timestamp)

    def issue(self, interface, logger):
        self._do(interface)
        self._log(logger)

    def issue_counteraction(self, interface, logger):
        counter = self._get_counteraction()
        counter.issue(interface, logger)

    def _get_counteraction(self):
        raise NotImplementedError

    def _do(self, interface):
        raise NotImplementedError

    def _log(self, logger):
        logger.logAction(self.__class__.__name__, self.data)


class RunExp(Action):
    fields = {
        'exp_id'    : str,
        'end_epoch'     : int,
        'hyperparams': dict,
    }

    def _do(self, interface):
        interface.run_exp(self.data)

    def _get_counteraction(self):
        pass


class CounterAction(EventRecordable):
    "CounterAction should be idempotent"
    EVENTNAME_PREFIX = 'counter_'

    def _do(self, interface):
        raise NotImplementedError

    def _log(self, logger):
        raise NotImplementedError

    def issue(self, interface, logger):
        self._do(interface)
        self._log(logger)

    def get_orig_logid(self):
        return int(self.name.lstrip(CounterAction.EVENTNAME_PREFIX))
