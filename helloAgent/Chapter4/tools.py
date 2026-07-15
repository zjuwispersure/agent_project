import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

def search(query: str) -> str:
    """
    一个基于 Tavily Search API 的网页搜索引擎工具。
    需要设置 TAVILY_API_KEY 环境变量。
    """
    print(f"🔍 正在执行 [Tavily] 网页搜索: {query}")
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "错误:TAVILY_API_KEY 未设置环境变量。"

        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, search_depth="basic", include_answer=True)

        if response.get("answer"):
            return response["answer"]

        results = response.get("results", [])
        if not results:
            return f"对不起，没有找到关于 '{query}' 的信息。"

        snippets = [
            f"[{i+1}] {res.get('title', '')}\n{res.get('content', '')}"
            for i, res in enumerate(results[:5])
        ]
        return "\n\n".join(snippets)

    except Exception as e:
        return f"搜索时发生错误: {e}"

from typing import Dict, Any

class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools:
            print(f"警告:工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])
