from core.openai_service import OpenAIService
from mcp_client import MCPClient
from core.tools import ToolManager


class Chat:
    def __init__(self, openai_service: OpenAIService, clients: dict[str, MCPClient]):
        self.openai_service: OpenAIService = openai_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[dict] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        while True:
            response = self.openai_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            self.openai_service.add_assistant_message(self.messages, response)

            if response.choices[0].finish_reason == "tool_calls":
                print(self.openai_service.text_from_response(response))
                tool_results = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                self.openai_service.add_user_message(
                    self.messages, tool_results
                )
            else:
                final_text_response = self.openai_service.text_from_response(
                    response
                )
                break

        return final_text_response
