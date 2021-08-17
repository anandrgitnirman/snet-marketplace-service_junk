import json
from datetime import datetime as dt


class DemoComponent:
    def __init__(self, demo_component_required, demo_component_url=None, demo_component_status=None,
                 demo_component_last_modified=None):
        self._demo_component_url = demo_component_url
        self._demo_component_required = demo_component_required
        self._demo_component_status = demo_component_status
        self._demo_component_last_modified = demo_component_last_modified

    def to_dict(self):
        return {
            "demo_component_url": self._demo_component_url,
            "demo_component_required": self._demo_component_required,
            "demo_component_status": self._demo_component_status,
            "demo_component_last_modified": dt.isoformat(dt.fromisoformat(self._demo_component_last_modified)) if self._demo_component_last_modified else None
        }

    @property
    def demo_component_url(self):
        return self._demo_component_url

    @demo_component_url.setter
    def demo_component_url(self, demo_component_url):
        self._demo_component_url = demo_component_url

    @property
    def demo_component_required(self):
        return self._demo_component_required

    @demo_component_required.setter
    def demo_component_required(self, demo_component_required):
        self._demo_component_required = demo_component_required

    @property
    def demo_component_status(self):
        return self._demo_component_status

    @demo_component_status.setter
    def demo_component_status(self, demo_component_status):
        self._demo_component_status = demo_component_status

    @property
    def demo_component_last_modified(self):
        return self._demo_component_last_modified

    @demo_component_last_modified.setter
    def demo_component_last_modified(self, demo_component_last_modified):
        self._demo_component_last_modified = demo_component_last_modified
