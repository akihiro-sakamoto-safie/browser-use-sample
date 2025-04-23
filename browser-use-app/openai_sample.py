import asyncio

from browser_use import Agent
from langchain_openai import ChatOpenAI


async def main():
    agent = Agent(
        task="""
セーフィー公式サイトからカメラの情報を取得してください。
カメラの情報は、カメラの型番、価格、特徴を含めてください。
""",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result.final_result())


asyncio.run(main())
