import logging
from typing import Union

import anthropic
from jinja_helper import process_template

logging.basicConfig(level=logging.INFO)


class Claude:
    def __init__(self, api_key: str, max_tokens: int = 4096):
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20240620"
        self.max_tokens = max_tokens
        self.system = process_template("system.jinja", {})
        self.temperature = 0

    def _api(self, messages: list):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages
        )
        return message.content

    def ask_claude(self, message: dict):
        if message.get("action") != "chat":
            processed_message = process_template(f"{message.get('action')}.jinja", message)
        if message.get("think_twice_action") != None:
            processed_message += process_template(f"{message.get('think_twice_action')}.jinja", message)
        return self._api([{"role": "user", "content": processed_message}])
