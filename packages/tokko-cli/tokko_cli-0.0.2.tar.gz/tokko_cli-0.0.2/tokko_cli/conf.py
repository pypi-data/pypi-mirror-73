from configparser import ConfigParser
from dataclasses import dataclass
import os

from tokko_cli.utils import render

CONFIG_FILE_TEMPLATE = """{% for section in config.sections() %}
[{{ section }}]{% for key in config[section] %}
{{ key }} = {{ config[section][key] }}{% endfor %}
{% endfor %}
"""
DEFAULT_CONFIG = {
    "cli": {
        "is_initialized": False,
        "daemon_port": "9142",
        "daemon_host": "localhost",
    },
    "sources": {
        "monorepo_path": "",
        "remote": "git@github.com:TokkoLabs/services-tokkobroker.git",
    },
    "user": {
        "github_refresh_token": "",
        "refresh_token_expiration": "",
        "text_editor": "",
    }
}


@dataclass
class Settings:
    current_user: str

    def __post_init__(self):
        if not self.exists_user_config():
            self.create_conf()

    def __getattr__(self, section):

        class SettingSection:

            def __init__(self, main_conf: ConfigParser, handler: Settings, config_section: str):
                self.main_conf = main_conf
                self.handler = handler
                self.section = config_section

            def update(self, key, value):
                self.main_conf[self.section][key] = value
                self.handler.save(config=self.main_conf)

        config = self.load_config()

        try:
            for entry in config[section]:
                setattr(SettingSection, entry, config[section][entry])
            set_section = SettingSection(main_conf=config,
                                         handler=self,
                                         config_section=section)
            return set_section
        except KeyError:
            raise AttributeError(f"Settings has not {section} attribute")

    def get_config_path(self):
        return os.path.join(f"/home", self.current_user, ".tokko", "tokko-cli.conf")

    @staticmethod
    def get_default_conf() -> ConfigParser:
        default_config = ConfigParser()
        for section in DEFAULT_CONFIG:
            default_config[section] = DEFAULT_CONFIG[section]
        return default_config

    def exists_user_config(self) -> bool:
        return os.path.exists(self.get_config_path())

    def save(self, config):
        conf_filename = self.get_config_path()
        if not os.path.exists(os.path.dirname(conf_filename)):
            os.makedirs(os.path.dirname(conf_filename))
        with open(self.get_config_path(), "w") as config_file:
            config_file.write(render(CONFIG_FILE_TEMPLATE,
                                     **{"config": config}
                                     ))

    def create_conf(self):
        self.save(config=self.get_default_conf())

    def load_config(self) -> ConfigParser:
        config = ConfigParser()
        config.read(self.get_config_path())
        return config
