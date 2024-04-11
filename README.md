# post_images
Raspberry Piのカメラモジュールを用いて画像を撮影し、Discordにアップロードするプログラムです。
## 使い方
1.`get_post_images.py`と同じディレクトリに`.env`ファイルを作成し、Discord botのトークンおよびWEBHOOK URLを記述してください。不明な点は私(gomazarashi)にお問い合わせください。
Raspberry Piをインターネットに接続し、`get_post_images.py`を実行してください。今のところ5分に一度画像が撮影・投稿される設定ですが、自由にコードを書き換えて、変更してください。もし必要なモジュールがインストールされていない場合は、`pip install`コマンドを用いてインストールしてください。