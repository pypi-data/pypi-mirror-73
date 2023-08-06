import os
import pprint


class Config:
    class __Config:
        def __init__(self, env, path="/hub/backend"):
            self.data = {}
            self.conf_file_path = os.path.join(path, "conf/conf-{}.json".format(env))
            # with open(self.conf_file_path) as configFile:
            #    self.data = json.load(configFile)

        def __str__(self):
            pprint.pformat(self.data)

    instance = None

    def __init__(self, env="prod"):
        if os.environ.get("ENVIRONMENT") is not None:
            env = os.environ.get("ENVIRONMENT")

        if not Config.instance:
            Config.instance = Config.__Config(env)

    def show(self):
        pprint(Config.instance.data)

    def get(self, key):
        if key.upper() in os.environ and os.environ.get(key.upper()) is not None:
            return os.environ.get(key.upper())

        return Config.instance.data[key]
