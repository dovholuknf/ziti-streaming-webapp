# This file is part of ziti-streaming-webapp
# Copyright (c) 2024 Jacob Dybvald Ludvigsen (contributions@ingeniorskap.no)
# SPDX-License-Identifier: AGPL-3.0-or-later


class webConfigHolder:
    """
    Holds a dict of objects and variables that will be available to all
    functions in web_ui
    """

    def __init__(self):
        self.web_config = {}

    def update_config(self, input_dict):
        self.web_config.update(input_dict)

    def modify_key(self, key, value):
        self.web_config[key] = value

    def read_key(self, key):
        return self.web_config.get(key)
