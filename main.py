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

# EchoVRのexeパス。環境に合わせて変更してください。
ECHO_VR_EXE_PATH = "D:\\Oculus\\Software\\Software\\ready-at-dawn-echo-arena\\" + \
    "bin\\win10\\echovr.exe"
# QuestのIPアドレス。環境に合わせて変更してください。
QUEST_HOST = "192.168.1.1"
# ローカルのIPアドレス。変更する必要はありません。
LOCAL_HOST = "localhost"
# 作成するサーバーリージョンの既定値。必要に応じて変更してください。
DEFAULT_SERVER_REGION = "jp"
# EchoVRのconfigパス。基本的には変更する必要はありません。
ECHO_VR_CONFIG_PATH = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\rad\\loneecho\\settings_mp_v2.json"
# API呼び出し 再試行のインターバル。0に近づけるほどより頻繁にAPIを呼び出しますが、コンピューターに負荷がかかる可能性があります。
API_CALL_INTERVAL = 3
# Questでセッションに参加した際、割り当てるチームのID
# 1=オレンジ, 0=ブルー, -1=スペクテイター
QUEST_TEAM_ID = 1
# Questでセッションに参加した際、ゲームルールを変更するかどうか。
# ゲームルールは、default_gamerule.jsonで変更できます。
CHANGE_RULES_ON_JOIN = True
# [環境設定ここまで]


with open(ECHO_VR_CONFIG_PATH) as f:
    config = json.load(f)
    if not config["game"]["EnableAPIAccess"]:
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
            config["game"]["EnableAPIAccess"] = True
            with open(ECHO_VR_CONFIG_PATH, mode="w") as ff:
                json.dump(config, ff)
        elif selection == "exit":
            sys.exit(0)
        elif selection == "continue":
            pass


def create_session(region="jp"):
    subprocess.Popen(
        f"{ECHO_VR_EXE_PATH} -noovr -spectatorstream -level mpl_arena_a -region {region}")


def get_session_id():
    while True:
        try:
            response = requests.get(f"http://{LOCAL_HOST}:6721/session")
            if response.ok:
                return response.json()["sessionid"]
        except:
            pass
        time.sleep(API_CALL_INTERVAL)


def join_in_quest():
    while True:
        try:
            response = requests.post(
                f"http://{QUEST_HOST}:6721/join_session", json={"session_id": session_id, "team_idx": QUEST_TEAM_ID})
            if response.json()["err_code"] == 0:
                if CHANGE_RULES_ON_JOIN:
                    print("ゲームルールを設定中…")
                    set_rules()
                break
        except:
            pass
        time.sleep(API_CALL_INTERVAL)

def set_rules():
    with open("default_gamerule.json") as f:
        rules = json.load(f)
        while True:
            try:
                response = requests.post(
                    f"http://{QUEST_HOST}:6721/set_rules", json=rules
                )
                if response.json()["err_code"] == 0:
                    break
            except:
                pass
            time.sleep(API_CALL_INTERVAL)


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
    default=DEFAULT_SERVER_REGION
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
    "rules": ("ルールを設定します。", set_rules)
}
while True:
    cmd = input("> ")
    if cmd in commands:
        commands[cmd][1]()
    else:
        print("コマンドが見つかりませんでした。")
