# coding: utf-8

"""
    OGC Compliant IUDX Resource Server

    OGC compliant Features and Common API definitions. Includes Schema and Response Objects.

    The version of the OpenAPI document: 1.0.1
    Contact: info@iudx.org.in
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class StatusCode(str, Enum):
    """
    StatusCode
    """

    """
    allowed enum values
    """
    ACCEPTED = 'ACCEPTED'
    RUNNING = 'RUNNING'
    SUCCESSFUL = 'SUCCESSFUL'
    FAILED = 'FAILED'
    DISMISSED = 'DISMISSED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of StatusCode from a JSON string"""
        return cls(json.loads(json_str))


