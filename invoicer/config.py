import configparser
import os

import keyring

# Default description for work.  You can change this per client in the config file. The script will ask for each client.
DESCRIPTION = "Development and consulting services."


class Config:

    def __init__(self, config_file):
        self.config_parser = configparser.ConfigParser()
        self.config_file = config_file
        if os.path.isfile(config_file):
            self.config_parser.read(config_file)
        else:
            account_id = input("Please enter your Harvest account ID.\n")
            self.config_parser['Harvest'] = {'account_id': account_id}
            rate_str = input("Please enter your hourly rate.\n")
            self.config_parser['Billing'] = {'rate': rate_str}
            with open(config_file, 'w') as configfile:
                self.config_parser.write(configfile)

        key = keyring.get_password("invoicer", "harvest_key")
        if key is None:
            key = input("Please enter your Harvest API key.\n")
            keyring.set_password("invoicer", "harvest_key", key)

        self.account_id = self.config_parser['Harvest']['account_id']
        self.api_key = key
        self.rate = float(self.config_parser['Billing']['rate'])

    def get_description(self, client_name):
        client_key = client_name.replace(" ", "_").lower()
        try:
            description = self.config_parser.get("Descriptions", client_key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            p1 = f"Please enter a description for your work at {client_name}. Press enter for \"{DESCRIPTION}\": "
            description = (input(p1).strip() or DESCRIPTION)
            p2 = f"Would you like to save this description and not ask for {client_name} in the future? (y/n) "
            if input(p2) == "y":
                self.config_parser['Descriptions'] = {client_key: description}
                with open(self.config_file, 'w') as configfile:
                    self.config_parser.write(configfile)
        return description
