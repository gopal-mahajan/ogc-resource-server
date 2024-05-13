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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from openapi_client.models.link import Link
from openapi_client.models.tile_matrix_limits import TileMatrixLimits
from openapi_client.models.tile_matrix_set_item_crs import TileMatrixSetItemCrs
from openapi_client.models.tile_set_item_data_type import TileSetItemDataType
from typing import Optional, Set
from typing_extensions import Self

class TileSet(BaseModel):
    """
    A resource describing a tileset based on the OGC TileSet Metadata Standard. At least one of the 'TileMatrixSet',  or a link with 'rel' http://www.opengis.net/def/rel/ogc/1.0/tiling-scheme
    """ # noqa: E501
    title: Optional[StrictStr] = Field(default=None, description="A title for this tileset")
    description: Optional[StrictStr] = Field(default=None, description="Brief narrative description of this tile set")
    data_type: TileSetItemDataType = Field(alias="dataType")
    crs: TileMatrixSetItemCrs
    tile_matrix_set_uri: Optional[StrictStr] = Field(default=None, description="Reference to a Tile Matrix Set on an offical source for Tile Matrix Sets such as the OGC NA definition server (http://www.opengis.net/def/tms/). Required if the tile matrix set is registered on an open official source.", alias="tileMatrixSetURI")
    links: List[Link] = Field(description="Links to related resources. Possible link 'rel' values are: 'http://www.opengis.net/def/rel/ogc/1.0/dataset' for a URL pointing to the dataset, 'item' for a URL template to get a tile; 'alternate' for a URL pointing to another representation of the TileSetMetadata (e.g a TileJSON file); 'http://www.opengis.net/def/rel/ogc/1.0/tiling-scheme' for a definition of the TileMatrixSet; 'http://www.opengis.net/def/rel/ogc/1.0/geodata' for pointing to a single collection (if the tileset represents a single collection)")
    tile_matrix_set_limits: Optional[List[TileMatrixLimits]] = Field(default=None, description="Limits for the TileRow and TileCol values for each TileMatrix in the tileMatrixSet. If missing, there are no limits other that the ones imposed by the TileMatrixSet. If present the TileMatrices listed are limited and the rest not available at all", alias="tileMatrixSetLimits")
    __properties: ClassVar[List[str]] = ["title", "description", "dataType", "crs", "tileMatrixSetURI", "links", "tileMatrixSetLimits"]

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
        """Create an instance of TileSet from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of data_type
        if self.data_type:
            _dict['dataType'] = self.data_type.to_dict()
        # override the default output from pydantic by calling `to_dict()` of crs
        if self.crs:
            _dict['crs'] = self.crs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tile_matrix_set_limits (list)
        _items = []
        if self.tile_matrix_set_limits:
            for _item in self.tile_matrix_set_limits:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tileMatrixSetLimits'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TileSet from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "title": obj.get("title"),
            "description": obj.get("description"),
            "dataType": TileSetItemDataType.from_dict(obj["dataType"]) if obj.get("dataType") is not None else None,
            "crs": TileMatrixSetItemCrs.from_dict(obj["crs"]) if obj.get("crs") is not None else None,
            "tileMatrixSetURI": obj.get("tileMatrixSetURI"),
            "links": [Link.from_dict(_item) for _item in obj["links"]] if obj.get("links") is not None else None,
            "tileMatrixSetLimits": [TileMatrixLimits.from_dict(_item) for _item in obj["tileMatrixSetLimits"]] if obj.get("tileMatrixSetLimits") is not None else None
        })
        return _obj


