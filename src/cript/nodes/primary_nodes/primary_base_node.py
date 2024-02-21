from abc import ABC
from dataclasses import dataclass, replace
import json
from jsonschema import validate as jsonschema_validate

from beartype import beartype

from cript.nodes.uuid_base import UUIDBaseNode

import cript
import requests
from cript.api.api_config import _API_TIMEOUT
import datetime
from deepdiff import DeepDiff


# WIP : we will load in these values from a config file or .env
class Config:
    host = "https://lb-stage.mycriptapp.org"
    token = ""
    storage_token = ""


class PrimaryBaseNode(UUIDBaseNode, ABC):
    """
    Abstract class that defines what it means to be a PrimaryNode,
    and other primary nodes can inherit from.
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        """
        All shared attributes between all Primary nodes and set to their default values
        """

        locked: bool = False
        model_version: str = ""
        public: bool = False
        name: str = ""
        notes: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, name: str, notes: str, **kwargs):
        # initialize Base class with node
        super().__init__(**kwargs)
        # replace name and notes within PrimaryBase
        self._json_attrs = replace(self._json_attrs, name=name, notes=notes)

    @classmethod
    def create_with_uuid(cls, uuid, name, **kwargs):
        # Instantiate the object with given name, notes, and any additional keyword arguments.
        obj = cls(name, **kwargs)
        # Directly set the _uuid attribute. Consider modifying the base class to allow this, or use an appropriate setter.
        obj._uuid = uuid  # This assumes there's a mechanism to set _uuid directly or indirectly in the base class.
        return obj

    @beartype
    def __str__(self) -> str:
        """
        Return a string representation of a primary node dataclass attributes.
        Every node that inherits from this class should overwrite it to best fit
        their use case, but this provides a nice default value just in case

        Examples
        --------
        {
        'locked': False,
        'model_version': '',
        'public': False,
        'notes': ''
        }


        Returns
        -------
        str
            A string representation of the primary node common attributes.
        """
        return super().__str__()

    @property
    @beartype
    def locked(self):
        return self._json_attrs.locked

    @property
    @beartype
    def model_version(self):
        return self._json_attrs.model_version

    @property
    @beartype
    def updated_by(self):
        return self._json_attrs.updated_by

    @property
    @beartype
    def created_by(self):
        return self._json_attrs.created_by

    @property
    @beartype
    def public(self):
        return self._json_attrs.public

    @property
    @beartype
    def name(self):
        return self._json_attrs.name

    @name.setter
    @beartype
    def name(self, new_name: str) -> None:
        """
        set the PrimaryBaseNode name

        Parameters
        ----------
        new_name: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def notes(self):
        return self._json_attrs.notes

    @notes.setter
    @beartype
    def notes(self, new_notes: str) -> None:
        """
        allow every node that inherits base attributes to set its notes
        """
        new_attrs = replace(self._json_attrs, notes=new_notes)
        self._update_json_attrs_if_valid(new_attrs)
