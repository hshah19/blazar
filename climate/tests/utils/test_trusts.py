# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from climate import context
from climate import tests
from climate.utils.openstack import base
from climate.utils.openstack import keystone
from climate.utils import trusts


class TestTrusts(tests.TestCase):
    def setUp(self):
        super(TestTrusts, self).setUp()
        self.base = base
        self.trusts = trusts
        self.context = context
        self.keystone = keystone

        self.client = self.patch(self.keystone, 'ClimateKeystoneClient')
        self.patch(self.context, 'current')
        self.patch(self.base, 'url_for').return_value = 'http://www.foo.fake'

    def test_create_trust(self):
        correct_trust = self.client().trusts.create()

        trust = self.trusts.create_trust()

        self.assertEqual(trust, correct_trust)

    def test_delete_trust(self):
        lease = mock.MagicMock(trust_id='1')

        self.trusts.delete_trust(lease)

        self.client.assert_called_once_with(trust_id='1')

    def test_create_ctx_from_trust(self):
        fake_item = self.client().service_catalog.catalog.__getitem__()
        fake_ctx_dict = {'_BaseContext__values': {
            'auth_token': self.client().auth_token,
            'service_catalog': fake_item,
            'project_id': self.client().tenant_id,
            'project_name': 'admin',
            'user_name': 'admin',
        }}

        ctx = self.trusts.create_ctx_from_trust('1')

        self.assertEqual(fake_ctx_dict, ctx.__dict__)

    def test_use_trust_auth_dict(self):
        def to_wrap(self, arg_to_update):
            return arg_to_update

        correct_trust = self.client().trusts.create()
        fill_with_trust_id = {}
        updated_arg = self.trusts.use_trust_auth()(to_wrap)(self,
                                                            fill_with_trust_id)
        self.assertIn('trust_id', updated_arg)
        self.assertEqual(correct_trust.id, updated_arg['trust_id'])

    def test_use_trust_auth_object(self):
        class AsDict(object):
            def __init__(self, value):
                self.value = value

            def as_dict(self):
                to_return = {}
                for key in dir(self):
                    to_return[key] = getattr(self, key)
                return to_return

        def to_wrap(self, arg_to_update):
            return arg_to_update

        correct_trust = self.client().trusts.create()
        fill_with_trust_id = AsDict(1)
        updated_arg = self.trusts.use_trust_auth()(to_wrap)(self,
                                                            fill_with_trust_id)
        self.assertIn('trust_id', updated_arg.as_dict())
        self.assertEqual(correct_trust.id, updated_arg.trust_id)
