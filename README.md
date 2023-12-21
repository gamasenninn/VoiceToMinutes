# VoiceToMinutes

## 概要
VoiceToMinutesは、動画または、音声録音をより扱いやすいテキストベースの議事録に変換することを目的としたPythonベースのプロジェクトです。このプロジェクトは、会議や講義、または任意のオーディオコンテンツを書面形式に転記し、より簡単に参照および分析したい専門家に適しています。
文字起こし、議事録の起草にはOpenAIのAPIを使用しています。

## 機能

- **オーディオ分割（`v2a_split.py`）**: 長いオーディオファイルを小さなセグメントに分割します。これは、大きな録音を管理したり、部分的に処理したりするのに役立ちます。
- **オーディオからテキストへの変換（`a2txt.py`）**: オーディオファイルをテキストに変換し、音声認識技術を活用します。このスクリプトは、話されたコンテンツを書面形式に転記するために不可欠です。
- **議事録作成（`make_minutes.py`）**: テキストデータを処理し、フォーマットと構造を正式な議事録として整えます。このスクリプトは、転記されたテキストをより読みやすく、正式な文書に整理するのに役立ちます。

## 使い始める

### 前提条件
- Python 3.x
- 必要なPythonライブラリ：　pydub,及びOpenAI APIライブラリ


### 使用方法
プロジェクト内の各スクリプトは、要件に応じて独立して実行できます。

#### オーディオ分割
```bash
python v2a_split.py <audio_file_path>
```
#### オーディオからテキストへの変換
```bash
python a2txt.py <audio_file_path>
```

#### 議事録作成
```bash
python make_minutes.py <text_data_directory>
```

## ライセンス
このプロジェクトは[MITライセンス](LICENSE)のもとでライセンスされています - 詳細はLICENSEファイルを参照してください。

