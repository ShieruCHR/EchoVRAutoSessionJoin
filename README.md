# EchoVRAutoSessionJoin
PCでEchoVRのセッションを建て、Questで参加します。  
セッションを建てたPC側のEchoVRは、スペクテイターとしてその場に居残り続けます。

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
