import json
import subprocess
import time
import requests
import os
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

#
# [ 環境設定 ]
#
# これらの設定は、プログラムを正しく動作させるために必要です。
# 各項目の説明を読みながら設定してください。

# [環境設定ここまで]

with open("settings.json", encoding="UTF-8") as f:
    config = json.load(f)
    if config.get("ECHO_VR_CONFIG_PATH") is None:
        config["ECHO_VR_CONFIG_PATH"] = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\rad\\loneecho\\settings_mp_v2.json"

with open(config.get("ECHO_VR_CONFIG_PATH")) as f:
    game_config = json.load(f)
    if not game_config["game"]["EnableAPIAccess"]:
        selection = inquirer.select(
            message="API アクセスが無効になっています。どうしますか？",
            choices=[
                Choice("enable", name="自動で設定を変更する"),
                Choice(
                    "exit", name="設定を変更せず、プログラムを終了する"),
                Choice(
                    "continue", name="設定を変更せず、このまま続行する")
            ]

        ).execute()
        if selection == "enable":
            game_config["game"]["EnableAPIAccess"] = True
            with open(config.get("ECHO_VR_CONFIG_PATH"), mode="w") as ff:
                json.dump(game_config, ff)
        elif selection == "exit":
            sys.exit(0)
        elif selection == "continue":
            pass


def create_session(region="jp"):
    subprocess.Popen(
        f"{config.get('ECHO_VR_EXE_PATH')} -noovr -spectatorstream -level mpl_arena_a -region {region}")


def get_session_id():
    while True:
        try:
            response = requests.get(f"http://{config.get('LOCAL_HOST')}:6721/session")
            if response.ok:
                return response.json()["sessionid"]
        except:
            pass
        time.sleep(config.get('API_CALL_INTERVAL'))


def join_in_quest():
    while True:
        try:
            response = requests.post(
                f"http://{config.get('QUEST_HOST')}:6721/join_session", json={"session_id": session_id, "team_idx": config.get('QUEST_TEAM_ID')})
            if response.json()["err_code"] == 0:
                if config.get("AUTO_RULES").get("enabled"):
                    print("ゲームルールを設定中…")
                    set_rules()
                break
        except:
            pass
        time.sleep(config.get('API_CALL_INTERVAL'))

def set_rules():
    rules = config.get("AUTO_RULES").get("rules")
    while True:
        try:
            response = requests.post(
                f"http://{config.get('QUEST_HOST')}:6721/set_rules", json=rules
            )
            if response.json()["err_code"] == 0:
                break
        except:
            pass
        time.sleep(config.get('API_CALL_INTERVAL'))


print("セッションを作成します…")
region = inquirer.select(
    message="リージョンを選択してください: ",
    choices=[
        Choice("uscn", "アメリカ中北部"),
        Choice("us-central-2", "アメリカ中部2"),
        Choice("us-central-3", "アメリカ中部3"),
        Choice("use", "アメリカ東部"),
        Choice("usw", "アメリカ西部"),
        Choice("euw", "ヨーロッパ"),
        Choice("jp", "日本"),
        Choice("aus", "オーストラリア"),
        Choice("sin", "シンガポール")
    ],
    default=config.get('DEFAULT_SERVER_REGION')
).execute()
create_session(region=region)

print("セッションIDを取得中…")
session_id = get_session_id()
print("セッションにQuestで参加中…")
join_in_quest()

print("完了！今からコマンド入力を待機します。コマンドのリストを見るには、helpと入力してください。")


def cmd_help():
    for command, value in commands.items():
        print(f" - {command}: {value[0]}")


commands = {
    "help": ("コマンドのリストを見ます。", cmd_help),
    "exit": ("プログラムを終了します。", lambda: sys.exit(0)),
    "rejoin": ("QuestでEchoVRのセッションに再参加します。", join_in_quest),
    "session": ("現在のセッションIDを確認します。", lambda: print(session_id)),
    "rules": ("ルールを再設定します。", set_rules)
}
while True:
    cmd = input("> ")
    if cmd in commands:
        commands[cmd][1]()
    else:
        print("コマンドが見つかりませんでした。")
