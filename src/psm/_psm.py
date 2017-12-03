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

import transitions

class PersistentStateMachine(transitions.Machine):
    @classmethod
    def srp(cls, interface, logger):
        "The legendary State Recovery Protocol (SRP)"
        state = logger.find_last_state()
        trigger = logger.find_last_trigger_after(state)
        tobe_countered_actions = logger.find_uncountered_actions_after(state)
        for i in tobe_countered_actions:
            i.issue_counteraction(interface, logger)

        data = logger.recover_psm_data()
        return state, trigger, data
