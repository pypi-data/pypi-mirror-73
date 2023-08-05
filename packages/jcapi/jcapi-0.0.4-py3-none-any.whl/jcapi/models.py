"""Models for JC."""
from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from .exceptions import JCError



class Device:
    """Object holding the state of JC."""
    id: int
    name: str
    dev_type: str
    state: bool


def update_from_dict(data: dict) -> "Device":
    """Return Device object from JC API response."""
    if "page" in data and data["page"]:
        offline = data.get("offline")
        dev_list = []
        for dev_id, device in data["page"].items():
            # for dev_id, device in enumerate(data["page"]):
            dev_type = device.get("type")
            name = device.get("attr").get("NAME")
            state = True if (device.get("value"))==1 else False
            if int(dev_id) > 5 and dev_type == "switch":
                dev_list.append(Device(id=int(dev_id), name=name, dev_type=dev_type, state=state))
        # dev_list.sort(key=lambda dev_list: dev_list.id)
        return dev_list
    else:
        raise JCError
