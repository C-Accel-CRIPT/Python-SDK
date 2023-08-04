from enum import Enum
from pathlib import Path


class CRIPTEnvironment(Enum):
    """
    CRIPT Server Environment
    This class is meant to make using `_get_config_file_path()` easier
        > instead of inputting raw string, the developer can input an enum with code auto-completion on IDEs
    """
    DEVELOPMENT: str = "development"
    STAGING: str = "staging"
    PRODUCTION: str = "production"


def _get_config_file_path(environment: CRIPTEnvironment) -> Path:
    """
    gets the correct file path object for the correct environment with correct values

    Parameters
    ----------
    environment: CRIPTEnvironment

    Returns
    -------
    Path
    """

    # config.json file path
    config_file_path: Path = Path(__file__).parent.parent / f"{environment.value}_config.json"

    return config_file_path
