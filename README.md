# EchoVRAutoSessionJoin
PCでEchoVRのセッションを建て、Questで参加します。  
セッションを建てたPC側のEchoVRは、スペクテイターとしてその場に居残り続けます。

# How to use
## Pythonのインストール
https://www.python.org/downloads/ から、最新の安定版Pythonをダウンロード、手順に従ってインストールしてください。  
`Add Python3.X to PATH` かなんかのチェックを入れておくと便利かもしれません。

## 設定する
後述する`Configuration`セクションをごにょごにょしながら設定してください。  
唯一、`ECHO_VR_EXE_PATH`に関しては円マーク（バックスラッシュ）を二枚重ねしないといけないことに注意してください。  
例:  
:x: `C:\Program Files\Oculus\Software\EchoVR\echovr.exe`
:o: `C:\\Program Files\\Oculus\\Software\\EchoVR\\echovr.exe`

`QUEST_HOST`の設定も必要です。Sparkから拾ってくるか、Questの設定から確認してください。

## ライブラリのインストール
> 元の環境を汚したくないってんならこの段階で仮想環境でも作ってください。

`main.py`があるフォルダのパスをコピーし、コマンドプロンプトで`cd <コピーしたパス>`を実行します。  
`pip install -r requirements.txt`を実行し、ゴニョゴニョ色々英語で出てきたらOKです。

フォルダパスのコピーについては、Googleと呼ばれる便利なサイトで教えてもらえます。  
[Google It!](https://www.google.com/search?q=windows+%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%83%91%E3%82%B9+%E3%82%B3%E3%83%94%E3%83%BC)

## 実行する
ここまですべてうまくいっているなら、`main.py`をダブルクリックで起動できるはずです。  
もし実行できないなら、`main.py`があるフォルダのパスをコピーして、コマンドプロンプトを開き、  
```bat
cd <コピーしたパス>
py main.py
```
で起動してください。

# トラブルシューティング
GitHubのIssueでも投げてくれれば対応します。

# Configuration
`settings.json`を、以下の説明を見ながら適切に設定してください。

|Key|Type|Description|
|---|---|---|
|ECHO_VR_EXE_PATH|NotNull String|EchoVRのexeパス|
|QUEST_HOST|NotNull String|QuestのIPアドレス|
|LOCAL_HOST|NotNull String|localhostのIPアドレス。通常、変更する必要はありません。|
|DEFAULT_SERVER_REGION|Nullable String (default="jp")|リージョン選択時、デフォルトで選択しているリージョン|
|ECHO_VR_CONFIG_PATH|Nullable String|EchoVRのconfigパス。nullの場合、ユーザー名からconfigを自動取得します。|
|API_CALL_INTERVAL|NotNull Integer|APIの呼び出し間隔。単位は秒数です。小さい値の場合、コンピューターに負荷がかかるかもしれません。|
|QUEST_TEAM_ID|NotNull Integer|Questでセッションに入る際に選択されるチーム。0=ブルー, 1=オレンジ, -1=スペクテイターです。|
|AUTO_RULES|NotNull Dictionary|ルールの自動設定を構成します。|

## AUTO_RULES
|Key|Type|Description|
|---|---|---|
|enabled|NotNull boolean|ルールの自動設定機能を有効化するかどうか。|
|rules|NotNull Dictionary|設定するルール。勘とノリと勢いで決定してください。|
