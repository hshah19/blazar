# vim: tabstop=4 shiftwidth=4 softtabstop=4
# -*- encoding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Utils for testing the API service.
"""

import datetime
import json

from climate.openstack.common import timeutils

ADMIN_TOKEN = '4562138218392831'
MEMBER_TOKEN = '4562138218392832'


class FakeMemcache(object):
    """Fake cache that is used for keystone tokens lookup."""

    def __init__(self):
        self.set_key = None
        self.set_value = None
        self.token_expiration = None

        # Expire date will be updated in get()
        self.dt = datetime.datetime.utcnow() + datetime.timedelta(days=365)

        self._cache = {
            'tokens/%s' % ADMIN_TOKEN: {
                'access': {
                    'token': {'id': ADMIN_TOKEN,
                              'expires': timeutils.isotime(self.dt)},
                    'user': {'id': 'user_id1',
                             'name': 'user_name1',
                             'tenantId': '123i2910',
                             'tenantName': 'mytenant',
                             'roles': [{'name': 'admin'}]},
                }
            },
            'tokens/%s' % MEMBER_TOKEN: {
                'access': {
                    'token': {'id': MEMBER_TOKEN,
                              'expires': timeutils.isotime(self.dt)},
                    'user': {'id': 'user_id2',
                             'name': 'user-good',
                             'tenantId': 'project-good',
                             'tenantName': 'goodies',
                             'roles': [{'name': 'Member'}]},
                }
            }
        }

    def get(self, key):
        return json.dumps((self._cache.get(key), self.dt.isoformat()))

    def set(self, key, value, time=0):
        self.set_value = value
        self.set_key = key
