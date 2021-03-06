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

from keystoneclient import client as keystone_client

from climate import context
from climate import tests
from climate.utils.openstack import base
from climate.utils.openstack import keystone


class TestCKClient(tests.TestCase):

    def setUp(self):
        super(TestCKClient, self).setUp()

        self.keystone = keystone
        self.context = context
        self.k_client = keystone_client
        self.base = base

        self.ctx = self.patch(self.context, 'current')
        self.client = self.patch(self.k_client, 'Client')
        self.patch(self.base, 'url_for').return_value = 'http://fake.com/'

        self.version = '1'
        self.username = 'fake_user'
        self.token = 'fake_token'
        self.password = 'fake_pass'
        self.tenant_name = 'fake_project'
        self.auth_url = 'fake_url'
        self.trust_id = 'fake_trust'

    def test_client_from_kwargs(self):

        self.ctx.side_effect = RuntimeError

        self.keystone.ClimateKeystoneClient(version=self.version,
                                            username=self.username,
                                            password=self.password,
                                            tenant_name=self.tenant_name,
                                            trust_id=self.trust_id,
                                            auth_url=self.auth_url)

        self.client.assert_called_once_with(version=self.version,
                                            trust_id=self.trust_id,
                                            username=self.username,
                                            password=self.password,
                                            auth_url=self.auth_url)

    def test_client_from_kwargs_and_ctx(self):

        self.keystone.ClimateKeystoneClient(version=self.version,
                                            username=self.username,
                                            password=self.password,
                                            tenant_name=self.tenant_name,
                                            auth_url=self.auth_url)

        self.client.assert_called_once_with(version=self.version,
                                            tenant_name=self.tenant_name,
                                            endpoint='http://fake.com/',
                                            username=self.username,
                                            password=self.password,
                                            auth_url=self.auth_url)

    def test_client_from_ctx(self):

        self.keystone.ClimateKeystoneClient()

        self.client.assert_called_once_with(
            version='3',
            username=self.ctx().user_name,
            token=self.ctx().auth_token,
            tenant_name=self.ctx().project_name,
            auth_url='http://fake.com/',
            endpoint='http://fake.com/')

    def test_getattr(self):
        # TODO(n.s.): Will be done as soon as pypi package will be updated
        pass
