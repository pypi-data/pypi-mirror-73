# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
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
#
# ------------------------------------------------------------------------------

"""This module contains the tests of the gym connection module."""

import logging

import gym

import pytest

from aea.configurations.base import ConnectionConfig
from aea.identity.base import Identity
from aea.mail.base import Envelope

from packages.fetchai.connections.gym.connection import GymChannel, GymConnection
from packages.fetchai.protocols.gym.message import GymMessage

from tests.conftest import UNKNOWN_PROTOCOL_PUBLIC_ID

logger = logging.getLogger(__name__)


class TestGymConnection:
    """Test the packages/connection/gym/connection.py."""

    @classmethod
    def setup_class(cls):
        """Initialise the class."""
        cls.env = gym.GoalEnv()
        configuration = ConnectionConfig(connection_id=GymConnection.connection_id)
        identity = Identity("name", address="my_key")
        cls.gym_con = GymConnection(
            gym_env=cls.env, identity=identity, configuration=configuration
        )
        cls.gym_con.channel = GymChannel("my_key", gym.GoalEnv())
        cls.gym_con._connection = None

    def test_gym_connection_initialization(self):
        """Test the connection None return value after connect()."""
        self.gym_con.channel._queues["my_key"] = None
        assert self.gym_con.channel.connect() is None

    def test_decode_envelope_error(self):
        """Test the decoding error for the envelopes."""
        envelope = Envelope(
            to="_to_key",
            sender="_from_key",
            protocol_id=UNKNOWN_PROTOCOL_PUBLIC_ID,
            message=b"hello",
        )
        with pytest.raises(ValueError):
            self.gym_con.channel._decode_envelope(envelope)

    @pytest.mark.asyncio
    async def test_send_connection_error(self):
        """Test send connection error."""
        msg = GymMessage(
            performative=GymMessage.Performative.ACT,
            action=GymMessage.AnyObject("any_action"),
            step_id=1,
        )
        msg.counterparty = "_to_key"
        envelope = Envelope(
            to="_to_key",
            sender="_from_key",
            protocol_id=GymMessage.protocol_id,
            message=msg,
        )

        self.gym_con.connection_status.is_connected = False
        with pytest.raises(ConnectionError):
            await self.gym_con.send(envelope)

    @pytest.mark.asyncio
    async def test_receive_connection_error(self):
        """Test receive connection error and Cancel Error."""
        with pytest.raises(ConnectionError):
            await self.gym_con.receive()
