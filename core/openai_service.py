from openai import OpenAI


class OpenAIService:
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model

    def add_user_message(self, messages: list, content):
        if isinstance(content, list):
            messages.extend(content)
        else:
            messages.append({"role": "user", "content": content})

    def add_assistant_message(self, messages: list, response):
        msg = response.choices[0].message
        entry = {"role": "assistant", "content": msg.content}
        if msg.tool_calls:
            entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        messages.append(entry)

    def text_from_response(self, response) -> str:
        return response.choices[0].message.content or ""

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=None,
        tools=None,
    ):
        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        params = {
            "model": self.model,
            "max_completion_tokens": 8000,
            "messages": all_messages,
            "temperature": temperature,
        }

        if stop_sequences:
            params["stop"] = stop_sequences

        if tools:
            params["tools"] = tools

        return self.client.chat.completions.create(**params)
