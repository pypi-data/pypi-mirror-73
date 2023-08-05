# This file exists within 'dob-viewer':
#
#   https://github.com/tallybark/dob-viewer
#
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

"""Facts Carousel"""

from dob_bright.crud.fact_dressed import FactDressed

__all__ = (
    'FactsManager_Gap',
)


class FactsManager_Gap(object):
    """"""

    def fact_from_interval_gap(self, since_time, until_time):
        self.controller.affirm((not until_time) or (since_time < until_time))
        self.last_fact_pk -= 1
        gap_fact = FactDressed.new_gap_fact(
            pk=self.last_fact_pk,
            start=since_time,
            end=until_time,
        )
        # Add to undo stack. Sorta tricky. Sorta a hack.
        self.on_insert_fact(gap_fact)
        return gap_fact

    def wire_two_facts_neighborly(self, fact_1, fact_2):
        self.controller.affirm(fact_1 < fact_2)
        self.controller.affirm(fact_2.prev_fact is None)
        self.controller.affirm(fact_1.next_fact is None)
        fact_1.next_fact = fact_2
        fact_2.prev_fact = fact_1

