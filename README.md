# editLogs

## 動作確認環境

Windows 10

## chgSep.exe

対象フォルダ内のファイルを再帰的に全て読み取り、CSV形式ファイルのセパレータを変更して指定フォルダ内にファイル出力する。
対応セパレータはカンマ、タブ、スペース。スペース区切りの場合は連続するスペースを1つのセパレータとみなす。

## replaceOnDict.exe

対象フォルダ内のファイルを再帰的に全て読み取り、置換前後の文字列が記載された一覧ファイルに従って置換したファイルを指定フォルダ内に出力します。

## インストール

「editLogs_v20.zip」を任意の場所に解凍する。<br>
※ここでは「C:\tmp」に解凍する前提で記載する。

## chgSep.exe 実行

1. 設定ファイル C:\tmp\editLogs\conf\chgSep\ChgSep.conf を編集する。<br>
※設定ファイルの文字コードは「UTF8」としてください。
※設定ファイルは任意のパス、ファイル名でも問題ありません。

2. 設定ファイルのパラメータ「SOURCE_DIR」に指定したフォルダに変換対象ファイルを格納する。

3. コマンドプロンプトを起動して以下を実行する。<br>
`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep.conf`<br>
※実行ファイル及び設定ファイルは相対パスで実行しても問題ありません。
※設定ファイルを任意のパス、名前とした場合はそれを第一引数に指定してください。

4. 設定ファイル のパラメータ「WRITE_DIR」に指定したフォルダに変換後ファイルが格納されていることを確認する。

## replaceOnDict.exe 実行

1. 設定ファイル C:\tmp\editLogs\conf\replaceOnDict\replaceOnDict.conf を編集する。<br>
※設定ファイルの文字コードは「UTF8」としてください。
※設定ファイルは任意のパス、ファイル名でも問題ありません。

2. 置換文字列リストTSVファイル C:\tmp\editLogs\conf\replaceOnDict\replaceList.tsvを編集する。<br>
※置換文字列リストTSVファイルの文字コードは「UTF8」としてください。<br>
※置換文字列リストTSVファイルは設定ファイルの「REPLACE_LIST_FILE」に任意のファイルパス、名前を指定できます。

3. 設定ファイルのパラメータ「SEARCH_DIR」に指定したフォルダに変換対象ファイルを格納する。

4. コマンドプロンプトを起動して以下を実行する。<br>
`> C:\tmp\editLogs\bin\replaceOnDict.exe C:\tmp\editLogs\conf\replaceOnDict\replaceOnDict.conf`<br>
※実行ファイル及び設定ファイルは相対パスで実行しても問題ありません。
※設定ファイルを任意のパス、名前とした場合はそれを第一引数に指定してください。

5. 設定ファイル のパラメータ「WRITE_DIR」に指定したフォルダに変換後ファイルが格納されていることを確認する。

## サンプルの実行

### replaceOnDictサンプル実行

`> C:\tmp\editLogs\bin\replaceOnDict.exe ../conf/replaceOnDict/replaceOnDict.conf`<br>

### chgSepサンプル実行 CSVをTSVに変換

`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep.conf`<br>

### chgSepサンプル実行 TSVをCSVに変換

`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep_TSV2CSV.conf`<br>

### chgSepサンプル実行 Apacheアクセスログのスペース区切りをTSVに変換

`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep_access_log_SPACE2TAB.conf`<br>

### chgSepサンプル実行 netstatコマンド実行結果のスペース区切りをTSVに変換

`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep_netstat_SPACE2TAB.conf`<br>

### chgSepサンプル実行 psコマンド実行結果のスペース区切りをTSVに変換

`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep_ps_SPACE2TAB.conf`<br>

### chgSepサンプル実行 topコマンド実行結果のスペース区切りをTSVに変換

`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep_top_SPACE2TAB.conf`<br>

### chgSepサンプル実行 CSVをTSVに変換　文字コード変換込み

`> C:\tmp\editLogs\bin\chgSep.exe C:\tmp\editLogs\conf\chgSep\chgSep_enctest.conf`<br>

