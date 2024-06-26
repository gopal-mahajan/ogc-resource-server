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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from openapi_client.models.catalog_landing_page_links_inner import CatalogLandingPageLinksInner
from openapi_client.models.item import Item
from typing import Optional, Set
from typing_extensions import Self

class StacFeatureCollectionGeoJSON(BaseModel):
    """
    StacFeatureCollectionGeoJSON
    """ # noqa: E501
    type: StrictStr
    features: List[Item]
    links: Optional[List[CatalogLandingPageLinksInner]] = None
    time_stamp: Optional[datetime] = Field(default=None, description="This property indicates the time and date when the response was generated.", alias="timeStamp")
    number_matched: Optional[Annotated[int, Field(strict=True, ge=0)]] = Field(default=None, description="The number of features of the feature type that match the selection parameters like `bbox`.", alias="numberMatched")
    number_returned: Optional[Annotated[int, Field(strict=True, ge=0)]] = Field(default=None, description="The number of features in the feature collection.  A server may omit this information in a response, if the information about the number of features is not known or difficult to compute.  If the value is provided, the value shall be identical to the number of items in the \"features\" array.", alias="numberReturned")
    __properties: ClassVar[List[str]] = ["type", "features", "links", "timeStamp", "numberMatched", "numberReturned"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['FeatureCollection']):
            raise ValueError("must be one of enum values ('FeatureCollection')")
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
        """Create an instance of StacFeatureCollectionGeoJSON from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in features (list)
        _items = []
        if self.features:
            for _item in self.features:
                if _item:
                    _items.append(_item.to_dict())
            _dict['features'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of StacFeatureCollectionGeoJSON from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "features": [Item.from_dict(_item) for _item in obj["features"]] if obj.get("features") is not None else None,
            "links": [CatalogLandingPageLinksInner.from_dict(_item) for _item in obj["links"]] if obj.get("links") is not None else None,
            "timeStamp": obj.get("timeStamp"),
            "numberMatched": obj.get("numberMatched"),
            "numberReturned": obj.get("numberReturned")
        })
        return _obj


