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


class Event(object):
    def __init__(self, event_id, timestamp, event_type, event_name, data):
        self.event_id = event_id
        self.timestamp = timestamp
        self.event_type = event_type
        self.event_name = event_name
        self.data = data

    @classmethod
    def from_dict(cls, dic):
        return Event(dic['event_id'],
                     dic['timestamp'],
                     dic['event_type'],
                     dic['event_name'],
                     dic['data']
                    )


class EventRecordable(object):
    "Serves as the base class for any event type that is recordable event log"
    def __init__(self):
        pass

    @classmethod
    def recoverSpecific(cls, event):
        raise NotImplementedError

    def _log(self, logger):
        raise NotImplementedError

    @classmethod
    def from_event(cls, event):
        "Based on Event Type dispatch event recovery to each Type's handle"
        subclses = cls.__subclasses__()
        for subcls in subclses:
            if subcls.__name__ == event.event_type:
                return subcls.recoverType(event)
        raise ValueError('Log event type <{}> not understood'.format(event.event_type))

    @classmethod
    def recoverType(cls, event):
        "Based on Event Name dispatch event recovery to each specific event's handle"
        subclses = cls.__subclasses__()
        for subcls in subclses:
            if subcls.__name__ == event.event_name:
                return subcls.recoverSpecific(event)
        msg = "Event name <{}> not understood for type <{}>"
        raise ValueError(msg.format(event.event_name, event.event_type))
