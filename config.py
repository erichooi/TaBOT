import yaml

def get_yml_section(section):
    """
    :param string section: section of the ymlfile that need to return
    :return:
    """
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg[section]
