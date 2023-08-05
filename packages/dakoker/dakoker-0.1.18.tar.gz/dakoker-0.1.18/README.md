[![PyPI](https://img.shields.io/pypi/v/dakoker.svg)](https://pypi.python.org/pypi/dakoker)

MF-Dakoker
=======

[MFクラウド勤怠](https://biz.moneyforward.com/attendance)利用者向けに作った打刻・勤怠状況確認ツールです。

主な機能
- MFクラウド勤怠へのログイン
- 出勤・退勤の打刻
- 休憩開始・終了の打刻
- ログイン情報キャシュ・キャッシュクリア

実装予定機能
- 二重打刻の防止機能
- 過去・当日の勤怠状況の確認(打刻日時)
- Macユーザー向けにsafari driverを選択可能にする
  - chrome driverで問題が発生するユーザーが多そうであれば、safari driverも選択できると良さそうなため.

動作環境
- Python 3.8
- poetry 1.0.9

## How to Install
`pip3 install dakoker`

## Usage

- 出勤
  - `dakoker start`
- 退勤
  - `dakoker end`
- 休憩開始
  - `dakoker start_break`
- 休憩終了
  - `dakoker end_break`
- ログイン情報キャッシュのクリア
  - `dakoker clear`

### 初回利用時
ログインのため、以下の情報を入力します。

2回目以降は使用OSのパスワード保存領域(e.g. mac OSXであればキーチェーン上)・その他ローカル領域にキャッシュされたログイン情報を読み込み、自動ログインします。

- 企業ID
- ユーザーID もしくは登録メールアドレス
- パスワード

![初回ログイン時](https://gyazo.com/e0657a3eecfc6a486a469a0cebd98db1.png)
