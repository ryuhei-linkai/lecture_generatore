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

    with open("AIdocs/書籍生成AI.md", "r") as f:
        book_prompt = f.read()

    with open("syllabus.yaml", "r") as f:
        syllabus = f.read()

    with open("llms/claude.txt", "r") as f:
        claude_code = f.read()

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
                        "text": f"""

入力データ: 
{syllabus}

要件定義書:
{book_prompt}

上記の入力データと要件定義書をもとにして、Pythonのコードブロックのみ出力してください。

h1はクラスとして記述、h2はドキュメントとしてaisディレクトリにファイルとして格納
- aisディレクトリがなければ作成
- aisディレクトリ内にh2のドキュメントを記述（## の文字列を検知して、該当箇所をカットしてファイル保存）
with open("~~~.md", "w") as f:
    f.write(txt)
- この処理はpythonで記述しておくこと

クラス内でh2は以下の関数で適宜呼び出し。

from dotenv import load_dotenv
load_dotenv()  # .envファイルから環境変数を読み込む

利用LLM:
{claude_code}
    model="claude-3-haiku-20240307",
    max_tokens=200,
    temperature=0.5,

注意点:
- [ ] プログラムの進捗がわかるようなprintのコメントと、進捗バーを記載すること
"""
                    }
                ]
            }
        ]
    )
    return message.content[0].text



print("📚 本の生成コードを生成中...")
code = generate_book()
code = code.replace("```python", "").replace("```", "")
with open("generate_book.py", "w") as f:
    f.write(code)
print("✅ 本の生成コードを生成完了！")

print("📖 本の生成コードを実行中...")
# codeを実行するコードを追記
exec(code)
print("🎉 本の生成が完了しました！")
