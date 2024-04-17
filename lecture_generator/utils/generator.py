import os
from data.master_syllabus import generate_overview
import anthropic
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む

def generate_book():
    """
    """
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    # 🌸 messages contentの中にあるtextを変数として外に出しました
    with open("AIdocs/講義資料生成AI.md", "r") as f:
        lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.5,
        system="",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": lecture_content_prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def generate_lecture_content(lecture_title, lecture_description):
    """
    講義の内容を生成する関数

    Args:
        lecture_title (str): 講義のタイトル
        lecture_description (str): 講義の概要

    Returns:
        str: 生成された講義の内容（Markdown形式）

    講義のタイトルと概要を元に、以下の構成で講義の内容を生成します：
    1. 目次（リンク付き）
    2. 講義のタイトルと概要の説明（1000文字程度）
    3. 詳細解説（5つのトピックについて、各500文字程度）
    4. 各トピックの例題と解説

    専門用語は表形式でまとめ、わかりやすく説明します。
    """
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    # 🌸 messages contentの中にあるtextを変数として外に出しました
    with open("AIdocs/講義資料生成AI.md", "r") as f:
        lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.5,
        system="",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": lecture_content_prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text
def generate_quiz_content(lecture_title, lecture_description):
    """
    講義の問題集を生成する関数
    """
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    # 🌸 messages contentの中にあるtextを変数として外に出しました
    with open("AIdocs/quiz_content_prompt.md", "r") as f:
        quiz_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)
        print(quiz_content_prompt)

    message = client.messages.create(
        model="claude-3-opus-20240229",  # 使用するAIモデルの名前
        max_tokens=4000,  # AIが生成する最大の単語数
        temperature=0.5,  # 生成する文章のランダム性を調整するパラメータ
        system="",  # AIに事前に与える設定（ここでは空欄）
        messages=[  # AIに与える指示やコンテキストを設定
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": quiz_content_prompt
                    }
                ]
            }
        ]
    )

    return message.content[0].text
def generate_lectures(syllabus):
    """
    シラバスに基づいて講義資料を生成する関数
    
    Args:
        syllabus (list): シラバスのデータを含むリスト
        
    Returns:
        None
    """
    # 📁 outputディレクトリを作成（既に存在する場合はスキップ）
    os.makedirs("output", exist_ok=True)
    # 📅 シラバスの週の総数を取得
    total_weeks = len(syllabus)
    
    # 🔁 各週のデータに対してループ処理
    for week_num, week in enumerate(syllabus, start=1):
        # 📁 各週のディレクトリを作成（例: output/week1）
        week_dir = f"output/week{week['week']}"
        os.makedirs(week_dir, exist_ok=True)
        
        # 📝 各週のシラバスをMarkdownファイルに書き出し
        with open(f"{week_dir}/syllabus.md", "w") as f:
            f.write(f"# Week {week['week']} Syllabus\n\n")
            f.write("## Topics\n")
            for topic in week["topics"]:
                f.write(f"- {topic}\n")
        
        # 💬 現在の週の講義生成中であることを表示
        print(f"Week {week['week']}の講義を生成しています...")
        # 🔁 各講義のデータに対してループ処理
        for i, lecture in enumerate(tqdm(week["lectures"], desc=f"Week {week['week']}, Lecture"), start=1):
            # 📝 講義内容をMarkdownファイルに書き出し
            with open(f"{week_dir}/lecture{i}.md", "w") as f:
                f.write(f"# {lecture['title']}\n\n")
                lecture_content = generate_lecture_content(lecture["title"], lecture["description"])
                f.write(lecture_content)
            # ✅ 講義の生成完了メッセージを表示
            print(f"講義 {i} の生成が完了しました。")
            
            # 📝 問題集をMarkdownファイルに書き出し  
            with open(f"{week_dir}/quiz{i}.md", "w") as f:    
                quiz_content = generate_quiz_content(lecture["title"], lecture["description"])
                f.write("# 問題集\n\n")
                f.write(quiz_content)
            # ✅ 問題集の生成完了メッセージを表示
            print(f"問題集 {i} の生成が完了しました。")
        
        # 🎉 各週の処理完了メッセージを表示
        print(f"Week {week['week']} が完了しました。")
        # 📊 全体の進捗状況を表示
        print(f"進捗状況: {week_num}/{total_weeks} 週が完了しました。\n")

    # 📋 講義の概要を生成
    generate_overview()
    # 🎉 すべての講義の生成完了メッセージを表示
    print("すべての講義が正常に生成されました!")
