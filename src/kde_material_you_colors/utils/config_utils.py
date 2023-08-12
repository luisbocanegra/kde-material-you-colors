def get_config_value(config, config_name: str):
    if config != None:
        if config_name in config:
            return config[config_name]
