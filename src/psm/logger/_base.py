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
from datetime import datetime
import random

from psm import Event, EventRecordable
from psm import NUM_RANDOM_BITS
from psm.components import Action


class PersistentEventLogger(object):
    allowed_type = ['Trigger', 'EnterState', 'Action', 'CounterAction']

    def __init__(self, collection, if_mock=False):
        self.collection = collection
        self.if_mock = if_mock
        self._mocklogger = []
        self.curr_id = 0

    def records(self):
        "return a generator to the log"
        if self.if_mock:
            return self._mocklogger
        else:
            # use DB's generator
            raise NotImplementedError

    def empty(self):
        if self.if_mock:
            return not self._mocklogger
        else:
            raise NotImplementedError

    def logAnyEvent(self, typ, name, data=None, rand_stamp=None):
        self.curr_id += 1

        if typ not in PersistentEventLogger.allowed_type:
            error_msg = 'Persistent State Machine Error, event type <{}> not allowed to be logged!'
            raise ValueError(error_msg.format(typ))
        if not rand_stamp:
            rand_stamp = self.get_random_stamp()

        dic = { 'event_id'  : self.curr_id,
                'event_type': typ,
                'event_name': name,
                'rand_stamp': rand_stamp,
                'timestamp': datetime.now(),
                'data': data,
              }

        if self.if_mock:
            self._mocklogger.append(dic)
        else:
            self.collection.insert_one(dic)

    def get_random_stamp(self):
        random.seed(datetime.now())
        return random.getrandbits(NUM_RANDOM_BITS)

    def logEnterState(self, get_data_func, event, name=None):
        typ = 'EnterState'
        data = get_data_func()
        if not name:
            name = event.transition.dest
        self.logAnyEvent(typ, name, data=data)

    def logTrigger(self, name, data):
        typ = 'Trigger'
        self.logAnyEvent(typ, name, data)

    def logAction(self, name, data):
        typ = 'Action'
        self.logAnyEvent(typ, name, data)

    def logCounterAction(self, name, data):
        typ = 'CounterAction'
        self.logAnyEvent(typ, name, data)

    def printmocklog(self):
        for idx, record in enumerate(self._mocklogger):
            print(idx)
            print(record)
            print()

    def recover_psm_data(self):
        data = {'state':{}}
        for t in self._find_all_triggers():
            t.aggregate_data(data)
        for s in self._find_all_states():
            s.aggregate_data(data['state'])
        return data

    def _find_all_triggers(self):
        return self._find_all_type('Trigger')

    def _find_all_states(self):
        return self._find_all_type('EnterState')

    def _find_all_type(self, typ):
        all_this_type = []
        for i in self.records():
            if i['event_type'] == typ:
                dic = copy.deepcopy(i)
                event = Event.from_dict(dic)
                t = EventRecordable.from_event(event)
                all_this_type.append(t)
        return all_this_type

    def find_last_state(self):
        dic = None
        for i in self.records():
            if i['event_type'] == 'EnterState':
                dic = copy.deepcopy(i)
        if dic:
            event = Event.from_dict(dic)
            return EventRecordable.from_event(event)
        else:
            return None

    def find_last_trigger_after(self, state):
        dic = None
        state_is_found = False
        for i in self.records():
            if i['event_type'] == 'EnterState':
                state_is_found = True
            if state_is_found and i['event_type'] == 'Trigger':
                dic = copy.deepcopy(i)
        if dic:
            event = Event.from_dict(dic)
            return EventRecordable.from_event(event)
        else:
            return None

    def find_uncountered_actions_after(self, state):
        lst = self._find_actions_after(state)
        acts = [a for a in lst if not a.is_counter()]
        counteracts = [c for c in lst if c.is_counter()]

        counteracts_ids = [c.get_orig_logid() for c in counteracts]
        uncountered_actions = [a for a in acts if a.logid not in counteracts_ids]
        return uncountered_actions

    def _find_actions_after(self, state):
        "find actions (including counteractions) after a state in event log"
        actions = []
        state_is_found = False
        for i in self.records():
            if i['event_type'] == 'EnterState' and i['event_id'] == state.logid:
                state_is_found = True
            if state_is_found and i['event_type'] in ['Action', 'CounterAction']:
                dic = copy.deepcopy(i)
                event = Event.from_dict(dic)
                actions.append(Action.from_event(event))
        return actions
