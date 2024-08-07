"""
The `rendercv.data.reader` module contains the functions that are used to read the input
file (YAML or JSON) and return them as an instance of `RenderCVDataModel`, which is a
Pydantic data model of RenderCV's data format.
"""

import pathlib
from typing import Any

import ruamel.yaml

from . import models


def read_a_yaml_file(file_path_or_contents: pathlib.Path | str) -> dict[str, Any]:
    """Read a YAML file and return its content as a dictionary. The YAML file can be
    given as a path to the file or as the contents of the file as a string.

    Args:
        file_path_or_contents (pathlib.Path | str): The path to the YAML file or the
            contents of the YAML file as a string.
    Returns:
        dict: The content of the YAML file as a dictionary.
    """
    if isinstance(file_path_or_contents, pathlib.Path):
        # Check if the file exists:
        if not file_path_or_contents.exists():
            raise FileNotFoundError(
                f"The input file [magenta]{file_path_or_contents}[/magenta] doesn't"
                " exist!"
            )

        # Check the file extension:
        accepted_extensions = [".yaml", ".yml", ".json", ".json5"]
        if file_path_or_contents.suffix not in accepted_extensions:
            user_friendly_accepted_extensions = [
                f"[green]{ext}[/green]" for ext in accepted_extensions
            ]
            user_friendly_accepted_extensions = ", ".join(
                user_friendly_accepted_extensions
            )
            raise ValueError(
                "The input file should have one of the following extensions:"
                f" {user_friendly_accepted_extensions}. The input file is"
                f" [magenta]{file_path_or_contents}[/magenta]."
            )

        file_content = file_path_or_contents.read_text(encoding="utf-8")
    else:
        file_content = file_path_or_contents

    yaml_as_a_dictionary: dict[str, Any] = ruamel.yaml.YAML().load(file_content)

    return yaml_as_a_dictionary


def read_input_file(
    file_path_or_contents: pathlib.Path | str,
) -> models.RenderCVDataModel:
    """Read the input file (YAML or JSON) and return them as an instance of
    `RenderCVDataModel`, which is a Pydantic data model of RenderCV's data format.

    Args:
        file_path_or_contents (str): The path to the input file or the contents of the
            input file as a string.

    Returns:
        RenderCVDataModel: The data models with $\\LaTeX$ and Markdown strings.
    """
    input_as_dictionary = read_a_yaml_file(file_path_or_contents)

    # Validate the parsed dictionary by creating an instance of RenderCVDataModel:
    rendercv_data_model = models.RenderCVDataModel(**input_as_dictionary)

    return rendercv_data_model
