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
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from openapi_client.models.execute_inputs_value import ExecuteInputsValue
from typing import Optional, Set
from typing_extensions import Self

class Execute(BaseModel):
    """
    Execute
    """ # noqa: E501
    inputs: Optional[Dict[str, ExecuteInputsValue]] = None
    response: Optional[StrictStr] = 'raw'
    __properties: ClassVar[List[str]] = ["inputs", "response"]

    @field_validator('response')
    def response_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['raw', 'document']):
            raise ValueError("must be one of enum values ('raw', 'document')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Execute from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each value in inputs (dict)
        _field_dict = {}
        if self.inputs:
            for _key in self.inputs:
                if self.inputs[_key]:
                    _field_dict[_key] = self.inputs[_key].to_dict()
            _dict['inputs'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Execute from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "inputs": dict(
                (_k, ExecuteInputsValue.from_dict(_v))
                for _k, _v in obj["inputs"].items()
            )
            if obj.get("inputs") is not None
            else None,
            "response": obj.get("response") if obj.get("response") is not None else 'raw'
        })
        return _obj


