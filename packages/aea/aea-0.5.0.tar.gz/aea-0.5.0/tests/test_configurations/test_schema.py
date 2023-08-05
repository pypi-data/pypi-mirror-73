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

"""This test module contains the tests for the JSON schemas of the configuration files."""

import json
import os
from pathlib import Path

import jsonschema
from jsonschema import Draft4Validator, validate  # type: ignore

import pytest

import yaml

from aea.configurations.loader import make_jsonschema_base_uri

from ..conftest import (
    AGENT_CONFIGURATION_SCHEMA,
    CONFIGURATION_SCHEMA_DIR,
    CONNECTION_CONFIGURATION_SCHEMA,
    CUR_PATH,
    PROTOCOL_CONFIGURATION_SCHEMA,
    ROOT_DIR,
    SKILL_CONFIGURATION_SCHEMA,
    agent_config_files,
    connection_config_files,
    protocol_config_files,
    skill_config_files,
)


def test_agent_configuration_schema_is_valid_wrt_draft_04():
    """Test that the JSON schema for the agent configuration file is compliant with the specification Draft 04."""
    agent_config_schema = json.load(
        open(
            os.path.join(
                ROOT_DIR, "aea", "configurations", "schemas", "aea-config_schema.json"
            )
        )
    )
    Draft4Validator.check_schema(agent_config_schema)


def test_skill_configuration_schema_is_valid_wrt_draft_04():
    """Test that the JSON schema for the skill configuration file is compliant with the specification Draft 04."""
    skill_config_schema = json.load(
        open(
            os.path.join(
                ROOT_DIR, "aea", "configurations", "schemas", "skill-config_schema.json"
            )
        )
    )
    Draft4Validator.check_schema(skill_config_schema)


def test_connection_configuration_schema_is_valid_wrt_draft_04():
    """Test that the JSON schema for the connection configuration file is compliant with the specification Draft 04."""
    connection_config_schema = json.load(
        open(
            os.path.join(
                ROOT_DIR,
                "aea",
                "configurations",
                "schemas",
                "connection-config_schema.json",
            )
        )
    )
    Draft4Validator.check_schema(connection_config_schema)


def test_protocol_configuration_schema_is_valid_wrt_draft_04():
    """Test that the JSON schema for the protocol configuration file is compliant with the specification Draft 04."""
    protocol_config_schema = json.load(
        open(
            os.path.join(
                ROOT_DIR,
                "aea",
                "configurations",
                "schemas",
                "protocol-config_schema.json",
            )
        )
    )
    Draft4Validator.check_schema(protocol_config_schema)


def test_definitions_schema_is_valid_wrt_draft_04():
    """Test that the JSON schema for the definitions is compliant with the specification Draft 04."""
    definitions_config_schema = json.load(
        open(
            os.path.join(
                ROOT_DIR, "aea", "configurations", "schemas", "definitions.json"
            )
        )
    )
    Draft4Validator.check_schema(definitions_config_schema)


def test_validate_agent_config():
    """Test that the validation of the agent configuration file works correctly."""
    agent_config_file = yaml.safe_load(
        open(os.path.join(CUR_PATH, "data", "aea-config.example.yaml"))
    )
    agent_config_schema = json.load(open(AGENT_CONFIGURATION_SCHEMA))
    resolver = jsonschema.RefResolver(
        make_jsonschema_base_uri(Path(CONFIGURATION_SCHEMA_DIR)), agent_config_schema
    )
    validate(instance=agent_config_file, schema=agent_config_schema, resolver=resolver)


class TestAgentSchema:
    """Test that the agent configuration validation works."""

    @classmethod
    def setup_class(cls):
        """Set up the test class."""
        cls.schema = json.load(open(AGENT_CONFIGURATION_SCHEMA))
        cls.resolver = jsonschema.RefResolver(
            make_jsonschema_base_uri(Path(CONFIGURATION_SCHEMA_DIR).absolute()),
            cls.schema,
        )
        cls.validator = Draft4Validator(cls.schema, resolver=cls.resolver)

    @pytest.mark.parametrize("agent_path", agent_config_files)
    def test_validate_agent_config(self, agent_path):
        """Test that the validation of the protocol configuration file in aea/protocols works correctly."""
        protocol_config_file = yaml.safe_load(open(agent_path))
        self.validator.validate(instance=protocol_config_file)


class TestProtocolsSchema:
    """Test that the protocol configuration files provided by the framework are compliant to the schema."""

    @classmethod
    def setup_class(cls):
        """Set up the test class."""
        cls.schema = json.load(open(PROTOCOL_CONFIGURATION_SCHEMA))
        cls.resolver = jsonschema.RefResolver(
            make_jsonschema_base_uri(Path(CONFIGURATION_SCHEMA_DIR).absolute()),
            cls.schema,
        )
        cls.validator = Draft4Validator(cls.schema, resolver=cls.resolver)

    @pytest.mark.parametrize("protocol_path", protocol_config_files)
    def test_validate_protocol_config(self, protocol_path):
        """Test that the validation of the protocol configuration file in aea/protocols works correctly."""
        protocol_config_file = yaml.safe_load(open(protocol_path))
        self.validator.validate(instance=protocol_config_file)


class TestConnectionsSchema:
    """Test that the connection configuration files provided by the framework are compliant to the schema."""

    @classmethod
    def setup_class(cls):
        """Set up the test class."""
        cls.schema = json.load(open(CONNECTION_CONFIGURATION_SCHEMA))
        cls.resolver = jsonschema.RefResolver(
            make_jsonschema_base_uri(Path(CONFIGURATION_SCHEMA_DIR).absolute()),
            cls.schema,
        )
        cls.validator = Draft4Validator(cls.schema, resolver=cls.resolver)

    @pytest.mark.parametrize("connection_path", connection_config_files)
    def test_validate_connection_config(self, connection_path):
        """Test that the validation of the protocol configuration file in aea/protocols works correctly."""
        connection_config_file = yaml.safe_load(open(connection_path))
        self.validator.validate(instance=connection_config_file)


class TestSkillsSchema:
    """Test that the skill configuration files provided by the framework are compliant to the schema."""

    @classmethod
    def setup_class(cls):
        """Set up the test class."""
        cls.schema = json.load(open(SKILL_CONFIGURATION_SCHEMA))
        cls.resolver = jsonschema.RefResolver(
            make_jsonschema_base_uri(Path(CONFIGURATION_SCHEMA_DIR).absolute()),
            cls.schema,
        )
        cls.validator = Draft4Validator(cls.schema, resolver=cls.resolver)

    @pytest.mark.parametrize("skill_path", skill_config_files)
    def test_validate_skill_config(self, skill_path):
        """Test that the validation of the protocol configuration file in aea/protocols works correctly."""
        skill_config_file = yaml.safe_load(open(os.path.join(skill_path,)))
        self.validator.validate(instance=skill_config_file)
