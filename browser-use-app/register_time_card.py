import asyncio
import json
import os

import requests
from browser_use import Agent, AgentHistoryList
from browser_use.controller.service import Controller
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

controller = Controller()


class PostSettings(BaseModel):
    webhook_url: str
    name: str = "坂本 明優"


@controller.action("Slack通知", param_model=PostSettings)
def post_to_webhook(post_settings: PostSettings) -> None:
    response = requests.post(
        post_settings.webhook_url, json={"name": post_settings.name}
    )

    if response.status_code == 200:
        print("WebhookにPOSTしました。")
    else:
        print(f"WebhookのPOSTに失敗しました。ステータスコード: {response.status_code}")


async def main():
    agent = Agent(
        task=f"""
King of Time のタイムカード画面(https://s2.ta.kingoftime.jp/admin/)へアクセスし、現在の勤務状態を確認してください。

起動時点の日付でレコードを確認し、以下の条件で勤務状態を返してください。
- 出勤時間が登録されていなければ「未出勤」
- 出勤時間が登録されていて退勤時間が登録されていなければ「勤務中」
- 出勤時間と退勤時間が両方登録されていれば「退勤済」
また、出勤時間と退勤時間を取得してください。
結果は以下のようにJson形式で出力してください。

{{
    "status": "未出勤" | "勤務中" | "退勤済",
    "start_time": "出勤時間",
    "end_time": "退勤時間"
}}

勤務状態を取得するために、以下の手順で操作してください。
以下のフローで操作してください。
- King of Timeのタイムカード画面へアクセス
    - https://s2.ta.kingoftime.jp/admin/
- ログイン画面が表示された場合は、環境変数に設定した以下の値を入力後「OK」ボタンをクリックしてログインしてください。
    - {os.getenv("KOT_ID")}
    - {os.getenv("KOT_PASSWORD")}
- 「タイムカード」画面が表示されたら、以下の情報を取得してください。
    - 出勤時間
    - 退勤時間
    - 該当する日付がない場合はエラーメッセージを表示してください。
- 取得した情報を元に、勤務状態を判定してください。
- 勤務状態が取得できたらブラウザを閉じて、Slackへ通知を送信してください。
- 勤務状態が「未出勤」の場合は、{os.getenv("WORKING_START_WEBHOOK")}へSlack通知してください。
- 勤務状態が「勤務中」の場合は、{os.getenv("WORKING_END_WEBHOOK")}へSlack通知してください。
- 勤務状態が「退勤済」の場合は、何もしないでください。
- 取得した情報をJson形式で出力してください。
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        controller=controller,
    )

    result: AgentHistoryList = await agent.run()
    result_dict = json.loads(str(result.final_result()))
    print(result_dict)


if __name__ == "__main__":
    asyncio.run(main())
