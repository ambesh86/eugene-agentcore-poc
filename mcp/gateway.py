from mcp.registry import TOOLS


class MCPGateway:

    def invoke_tool(self,
                    tool_name,
                    *args,
                    **kwargs):

        tool = TOOLS.get(tool_name)

        if not tool:
            raise Exception(
                f"Tool {tool_name} not found"
            )

        return tool(
            *args,
            **kwargs
        )