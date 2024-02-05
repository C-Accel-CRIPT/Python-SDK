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


# WIP : we will load in these values from a config file
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

    # ================================================================================

    @classmethod
    def get_or_create(cls, node_type: str, object_name: str, **kwargs):
        host = Config.host
        token = Config.token

        if hasattr(cript, node_type.capitalize()):
            node_class = getattr(cript, node_type.capitalize())

            object_exists, uuid = cls.object_exists(node_type=node_type, object_name=object_name)

            if object_exists:
                node_data = cls.fetch_object_data(node_type, uuid)
                return node_class(**node_data, **kwargs)
            else:
                url = f"{host}/api/v1/{node_type}"
                data = {"node": [node_type.capitalize()], "name": object_name}
                headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

                response = requests.post(url, json=data, headers=headers)

                if response.status_code == 200:  # response for us when created
                    uuid = response.json()["data"]["result"][0].get("uuid")
                    node_data = cls.fetch_object_data(node_type, uuid)
                    return node_class(**node_data, **kwargs)
                elif response.status_code == 409:  # duplicate item
                    print("Duplicate item detected. Attempting to fetch existing item.")
                    # assuming the object now exists, attempt to fetch it again
                    _, uuid = cls.object_exists(node_type=node_type, object_name=object_name)
                    if uuid:
                        node_data = cls.fetch_object_data(node_type, uuid)
                        return node_class(**node_data, **kwargs)
                    else:
                        print("Failed to fetch the existing item after duplicate error.")
                        return None
                else:
                    # Handle other HTTP errors
                    print(f"Error during creation: {response.status_code}, {response.json()}")
                    return None
        else:
            raise ValueError(f"Invalid node type: {node_type}")

    @staticmethod
    def fetch_object_data(object_type: str, uuid: str):
        host = Config.host
        token = Config.token

        get_url = f"{host}/api/v1/{object_type.lower()}/{uuid}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        if response.json()["data"]:
            return response.json()["data"][0]  # Assuming the first item is the desired one
        else:
            return "Error"  # Consider raising an exception or returning None instead

    @classmethod
    def object_exists(cls, node_type: str, object_name: str):
        host = Config.host
        token = Config.token
        api_url = f"{host}/api/v1/{node_type}/"  # Ensure this URL lists all objects of the type
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            response = requests.get(api_url, headers=headers)

            response.raise_for_status()
            data = response.json()["data"]

            for item in data.get("result", []):
                if item.get("name") == object_name:
                    return True, item.get("uuid")
            return False, None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return False, None

    @staticmethod
    def load_schema_for_node_type(node_type):
        """
        Load the validation schema for a given node type.

        Args:
            node_type (str): The type of the node (e.g., 'Project', 'Material').

        Returns:
            dict: The loaded schema.
        """
        schema_file_path = f"src/cript/schemas/{node_type.lower()}_schema.json"  # Path to the schema file
        try:
            with open(schema_file_path, "r") as file:
                schema = json.load(file)
            return schema
        except FileNotFoundError:
            print(f"Schema file not found for node type: {node_type}")
            # Handle the error or raise an exception
        except json.JSONDecodeError:
            print(f"Invalid JSON format in schema file for node type: {node_type}")
            # Handle the error or raise an exception

    def get_schema(self):
        # Method to get the schema for validation.
        # This could be overridden in subclasses for specific schemas.
        return PrimaryBaseNode.load_schema_for_node_type(self.node_type)

    def patch(self, changes={}):
        # First, validate the changes against the schema
        schema = self.get_schema()

        jsonschema_validate(instance=changes, schema=schema)

        url = f"{Config.host}/api/v1/{self.node_type.lower()}/{self.uuid}"  # self.uuid project_uuid

        headers = {
            "Authorization": f"Bearer {Config.token}",
            "Content-Type": "application/json",
        }
        response = requests.patch(url, json=changes, headers=headers)

        return response

    # ===================== save method with helper functions ==================================================

    def save(self):
        # Fetch the original object data
        original = self.__class__.fetch_object_data(self.node_type, self.uuid)
        # original = {"node": original["node"]}

        # Use the current state of the object
        modified = self.get_json().json

        diff = DeepDiff(original, modified, ignore_order=True)
        diff_dict = diff.to_dict()

        diff_str = diff_dict["type_changes"]["root"]["new_value"]
        changes_for_patch = json.loads(diff_str)

        changes_for_patch.pop("uuid")
        changes_for_patch.pop("uid")

        self.patch(changes=changes_for_patch)

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
