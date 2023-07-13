#!/usr/bin/env python3

"""
Generates a template datapackage.json using w/ defaults of tides-data-package.json profile.

--output-path Saves it in the specified output directory (/path/to/output).
If the argument is not provided, it will default to the same directory as the script.

--yaml exports the template datapackage.json file as YAML instaed of JSON

--schema can alternately provide a separate schema
"""

import argparse
import json
import logging
import os
import jsonschema_default

USAGE = """
python samples/template/scripts/create_default_datapackage.py --output-dir /path/to/output
python generate_datapackage.py --output-dir /path/to/output --yaml
"""

SAMPLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_REPO_DIR = os.path.dirname(os.path.dirname(SAMPLE_DIR))
DEFAULT_SCHEMA = os.path.join(BASE_REPO_DIR, "spec", "tides-data-package.json")
DEFAULT_OUTPUT = "datapackage.json"


def generate_datapackage_from_defaults(
    schema_path: str = DEFAULT_SCHEMA,
    output_path: str = DEFAULT_OUTPUT,
    yaml: bool = False,
):
    """
    Generates a datapackage.json using structure and defaults of schema_file.

    args:
        schema_path: json-schema used for structuring file. Defaults
            to /spec/tides-data-package.json.
        output_path: where output will be put. Defaults to "datapackage.json"
        yaml: boolean indicating if output shoud be in YAML instead of JSON. Defaults to False.
    """
    logging.info(f"Generating default file from {schema_path}")
    with open(schema_path) as f:
        schema = json.load(f)

    # Generate the template datapackage using defaults
    datapackage = jsonschema_default.create_from(schema)

    # Write the template datapackage to a file
    if yaml:
        output_path = os.path.splitext(output_path)[0] + ".yaml"
        with open(output_path, "w") as f:
            yaml.dump(datapackage, f, sort_keys=False)
    else:
        with open(output_path, "w") as f:
            json.dump(datapackage, f, indent=2)

    print(f"Template datapackage file generated at: {output_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description="Generate a template datapackage file."
    )
    parser.add_argument(
        "--schema",
        default=DEFAULT_SCHEMA,
        help="Path to the JSON schema file (default: ../spec/tides-data-package.json)",
    )
    parser.add_argument(
        "--output-path",
        default=DEFAULT_OUTPUT,
        help="Directory to save the generated file (default: same directory as script)",
    )
    parser.add_argument(
        "--yaml", action="store_true", help="Export the file as YAML instead of JSON"
    )
    args = parser.parse_args()

    generate_datapackage_from_defaults(args.schema, args.output_path, args.yaml)
