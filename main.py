import os
import shutil
from datetime import datetime
from my_package.get_filename_list import get_filename_list
from my_package.get_image import get_image
from my_package.post_webhook import (
    post_text_discord,
    post_image_discord,
    post_text_slack,
)
from my_package.count_heads import count_heads
import csv
from time import sleep


def ensure_directories_exist(directories: list) -> None:
    """指定されたディレクトリが存在しなければ作成します"""
    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)


def clear_directory(directory: str) -> None:
    """ディレクトリ内の全てのファイルを削除します"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def move_image(from_folder: str, to_folder: str, image: str) -> None:
    """画像を指定されたフォルダに移動します"""
    try:
        shutil.move(os.path.join(from_folder, image), os.path.join(to_folder, image))
    except Exception as e:
        print(f"画像の移動中にエラーが発生しました: {e}")


def post_current_time() -> None:
    """現在の時刻をDiscordとSlackに投稿します"""
    current_time = datetime.now().strftime("%H:%M:%S")
    post_text_discord(f"現在の時刻は{current_time}です")
    post_text_slack("部室内人数通知システム", f"現在の時刻は{current_time}です")
    
def write_csv(now:datetime, count_heads_result:int) -> None:
    """CSVファイルに日時と人数を書き込みます"""
    now_yyyymm = now.strftime("%Y%m")
    now_str = now.strftime("%Y%m%d%H%M")
    
    # ディレクトリが存在しない場合は作成
    if not os.path.isdir("../data"):
        os.makedirs("../data")

    # ファイルが存在しない場合は作成
    if not os.path.exists(f"../data/headcount_{now_yyyymm}.csv"):
        with open(f"../data/headcount_{now_yyyymm}.csv", "w", encoding="utf-8", newline="") as f:
            data = [["datetime", "count_heads_result"], [now_str, count_heads_result]]
            writer = csv.writer(f)
            writer.writerows(data)
            print("ファイルを作成しました")

        # ファイルが存在する場合は追記 ロックされている場合は書き込みが成功するまで5回を上限に繰り返す
    else:
        max_retries = 5
        for i in range(max_retries):
            try:
                with open(f"../data/headcount_{now_yyyymm}.csv", "a", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([now_str, count_heads_result])
                    print("ファイルを追記しました")
                    break
            except PermissionError:
                print("ファイルがロックされています")
                if i == max_retries - 1:
                    print("ファイルの追記に失敗しました")
                else:
                    sleep(10)
            except Exception as e:
                print(f"ファイルの追記中にエラーが発生しました: {e}")
                break
    
# csvを読み込み最後と最後から二番目の人数を取得し、差があればTrueを返す
def is_people_changed(now:datetime)->bool:
    now_yyyymm = now.strftime("%Y%m")
    with open(f"../data/headcount_{now_yyyymm}.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        if len(rows) < 3:
            return True
        last_count = int(rows[-1][1])
        second_last_count = int(rows[-2][1])
        return last_count != second_last_count # 人数が変わっていればTrueを返す
    
    


def capture_and_process_image(now:datetime) -> None:
    """画像を撮影し、人数をカウントして結果を投稿します"""
    try:
        # 画像を撮影して保存
        get_image("shotten_images")

        # 画像のファイル名リストを取得
        images_list = get_filename_list("shotten_images")

        if not images_list:
            print("画像が存在しません")
            return

        image = images_list[0]

        # 人数をカウント
        count_heads_result = count_heads(
            os.path.join("shotten_images", image), "./my_package/best.pt"
        )
        
        write_csv(now, count_heads_result)
        
        # 人数が変わっていなければ画像を破棄して終了
        if not is_people_changed(now):
            print("人数が変わっていません")
            os.remove(os.path.join("shotten_images", image))
            return
        
        # 現在の時刻をDiscordとSlackに投稿
        post_current_time()

        # 画像をDiscordに投稿
        post_image_discord("shotten_images", image)

        # 画像を移動
        move_image("shotten_images", "posted_images", image)

        # 人数をDiscordとSlackに投稿
        post_text_discord(f"部室内の人数は{count_heads_result}人です")
        post_text_slack(
            "部室内人数通知システム", f"部室内の人数は{count_heads_result}人です"
        )

    except Exception as e:
        print(f"画像処理中にエラーが発生しました: {e}")


def start_job(now:datetime) -> None:
    """ジョブの開始を通知し、画像処理を実行します"""
    try:
        with open("./version.txt") as f:
            version = f.read()
        post_text_discord(f"現在のバージョンは{version}です\n画像の送信を開始します")
        post_text_slack(
            "部室内人数通知システム",
            f"現在のバージョンは{version}です\n画像の送信を開始します",
        )
        capture_and_process_image(now)
    except Exception as e:
        print(f"ジョブの開始中にエラーが発生しました: {e}")


def end_job(now:datetime) -> None:
    """ジョブの終了を通知し、画像処理を実行します"""
    try:
        capture_and_process_image(now)
        post_text_discord("画像の送信を終了します")
        post_text_slack("部室内人数通知システム", "画像の送信を終了します")
    except Exception as e:
        print(f"ジョブの終了中にエラーが発生しました: {e}")


def main() -> None:
    """メインの実行関数"""
    ensure_directories_exist(["shotten_images", "posted_images"])

    now = datetime.now().replace(second=0, microsecond=0)
    weekday = now.weekday()

    # 稼働時間の設定
    start_time = (
        now.replace(hour=8, minute=30)
        if weekday < 6
        else now.replace(hour=9, minute=30)
    )
    end_time = (
        now.replace(hour=22, minute=0)
        if weekday < 6
        else now.replace(hour=18, minute=0)
    )

    # 稼働時間に基づく処理
    if now < start_time or now > end_time:
        print("稼働時間外です")
    elif now == start_time:
        start_job(now)
    elif now == end_time:
        end_job(now)
    else:
        capture_and_process_image(now)


if __name__ == "__main__":
    main()
