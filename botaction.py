from types import SimpleNamespace

class APIBotActor(object):
    def __init__(self, bot, cfg, gw, api):
        self._gw = gw
        self.api = api

class APIBot(object):
    def __init__(self, cfg, gw, api):
        self._cfg = cfg
        self._gw = gw
        self._api = api

    def event(self, f):
        self._gw.event(f)

    def register_action(self, ctor, cfg_key=None):
        if cfg_key == None:
            ctor(self, None, self._gw, self._api)
            return
        if cfg_key not in self._cfg.actions:
            raise Exception(f"no cfg key {cfg_key}")
        cfg = SimpleNamespace(**self._cfg.actions[cfg_key])
        ctor(self, cfg, self._gw, self._api)

    def run(self):
        self._gw.run()

