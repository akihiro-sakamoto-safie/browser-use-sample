import asyncio

from browser_use import Agent
from langchain_anthropic import ChatAnthropic


async def main():
    agent = Agent(
        task="""
セーフィー公式サイトからカメラの情報を取得してください。
カメラの情報は、カメラの型番、価格、特徴を含めてください。
""",
        llm=ChatAnthropic(model_name="claude-3-5-haiku-20241022"),
    )
    result = await agent.run()
    print(result.final_result())


asyncio.run(main())
