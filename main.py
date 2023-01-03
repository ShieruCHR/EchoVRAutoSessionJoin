import json
import subprocess
import time
import requests
import os
import sys

# 
# [ 環境設定 ]
# 
# これらの設定は、プログラムを正しく動作させるために必要です。
# 各項目の説明を読みながら設定してください。

# EchoVRのexeパス。環境に合わせて変更してください。
ECHO_VR_EXE_PATH = "D:\\Oculus\\Software\\Software\\ready-at-dawn-echo-arena\\bin\\win10\\echovr.exe"
# QuestのIPアドレス。環境に合わせて変更してください。
QUEST_HOST = "192.168.1.1"
# ローカルのIPアドレス。変更する必要はありません。
LOCAL_HOST = "192.168.1.1"
# 作成するサーバーのリージョン。uscn, us-central-2, us-central-3, use, usw, euw, jp, aus, sinが許容されます。
# 必要に応じて変更してください。
SERVER_REGION = "jp"
# EchoVRのconfigパス。基本的には変更する必要はありません。
ECHO_VR_CONFIG_PATH = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\rad\\loneecho\\settings_mp_v2.json"

# [環境設定ここまで]



with open(ECHO_VR_CONFIG_PATH) as f:
    config = json.load(f)
    if not config["game"]["EnableAPIAccess"]:
        input("APIアクセスが無効になっているようです。Enterキーを押すと、自動で有効化します。変更したくない場合、Ctrl-Cでプログラムを終了してください。")
        config["game"]["EnableAPIAccess"] = True
        with open(ECHO_VR_CONFIG_PATH, mode="w") as ff:
            json.dump(config, ff)

def create_session():
    subprocess.Popen(f"{ECHO_VR_EXE_PATH} -noovr -spectatorstream -level mpl_arena_a -region {SERVER_REGION}")

def get_session_id():
    while True:
        try:
            response = requests.get(f"http://{LOCAL_HOST}:6721/session")
            if response.ok:
                return json.loads(response.content)["sessionid"]
        except:
            pass
        time.sleep(5)

def join_in_quest():
    while True:
        try:
            response = requests.post(f"http://{QUEST_HOST}:6721/join_session", json={"session_id": session_id, "team_idx": 1})
            if response.json()["err_code"] == 0:
                break
        except:
            pass
        time.sleep(5)


print("セッションを作成中…")
create_session()

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
    "exit": ("プログラムを終了します。EchoVRも終了します。", lambda: sys.exit(0)),
    "rejoin": ("QuestでEchoVRのセッションに再参加します。", join_in_quest),
    "session": ("現在のセッションIDを確認します。", lambda: print(session_id))
}
while True:
    cmd = input("> ")
    if cmd in commands:
        commands[cmd][1]()
    else:
        print("コマンドが見つかりませんでした。")

