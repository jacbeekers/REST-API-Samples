import json

import jsonschema

from metadata_utilities import messages, generic_settings, mu_logging


class CheckSchema:
    """
    Checks the JSON schema of a given JSON file
    """
    code_version = "0.2.15"

    def __init__(self):
        self.json_file = "not provided"
        self.json_data = ""
        self.meta_type = "unknown"
        self.meta_version = "unknown"
        self.schema_file = "unknown"
        self.mu_log = mu_logging.MULogging()
        self.settings = generic_settings.GenericSettings()

    def check_schema(self, data):
        """
        Checks the JSON to determine which JSON schema is used and which version
        """
        module = "check_schema"
        self.json_data = data

        try:
            self.meta_type = data["meta"]
            self.meta_version = data["meta_version"]
            self.mu_log.log(self.mu_log.DEBUG
                            , "schema is >" + self.meta_type + "<, version >"
                            + self.meta_version + "<", module)
        except KeyError as e:
            self.mu_log.log(self.mu_log.DEBUG,
                            "Key error. meta and meta_version must be in JSON file. That is not the case with "
                            + self.json_file, module)
            return messages.message["meta_error"]
        except jsonschema.exceptions.SchemaError as e:
            self.mu_log.log(self.mu_log.FATAL, "Schema error: " + e.message, module)
            return messages.message["json_schema_error"]
        except jsonschema.exceptions.ValidationError as e:
            self.mu_log.log(self.mu_log.FATAL, "Validation error: " + e.message, module)
            return messages.message["json_validation_error"]
        except json.decoder.JSONDecodeError as e:
            self.mu_log.log(self.mu_log.FATAL, "Error parsing JSON:" + e.msg, module)
            return messages.message["json_parse_error"]

        self.settings.get_config()
        schema_directory = self.settings.base_schema_folder + self.meta_version + "/"
        self.schema_file = schema_directory + self.meta_type + ".json"
        self.mu_log.log(self.mu_log.DEBUG, "schema_directory: " + schema_directory, module)
        self.mu_log.log(self.mu_log.DEBUG, "schema_file: " + self.schema_file)
        with open(self.schema_file) as f:
            schema = json.load(f)
            try:
                jsonschema.validate(data, schema)
                self.mu_log.log(self.mu_log.INFO, "JSON file validated successfully against schema", module)
            except jsonschema.exceptions.SchemaError as e:
                self.mu_log.log(self.mu_log.FATAL, "A schema error occurred during validation", module)
                return messages.message["jsonschema_validation_error"]
            except jsonschema.exceptions.ValidationError as e:
                self.mu_log.log(self.mu_log.ERROR, "A validation error occurred", module)
                return messages.message["jsonschema_validation_error"]

        return messages.message["ok"]
