from types import SimpleNamespace

class APIBotActor(object):
    def __init__(self, bot, cfg, gw, api):
        self._gw = gw
        self._cfg = cfg
        self.api = api
        self.bot = bot

class APIBot(object):
    def __init__(self, cfg, gw, api):
        self._cfg = cfg
        self._gw = gw
        self._api = api

    def _get_global_config(self):
        return self._cfg.shared

    def _get_config(self, key):
        # merge global config settings with action-specific ones
        global_cfg = self._get_global_config()
        if key == None:
            return SimpleNamespace(**global_cfg)
        if key not in self._cfg.actions:
            raise Exception(f"no config key actions.{key}")
        return SimpleNamespace(**global_cfg, **self._cfg.actions[key])

    def define_event_handler(self, f):
        self._gw.define_event_handler(f)

    def register_actor(self, ctor, cfg_key=None):
        cfg = self._get_config(cfg_key)
        ctor(self, cfg, self._gw, self._api)

    def run(self):
        self._gw.run()

    def log(self, content):
        self._api.run(f"/channels/{self._cfg.log_channel}/messages", "POST", {"content": content}) 

