
import os
import yaml
from dotenv import load_dotenv
import anthropic
from tqdm import tqdm

load_dotenv()  # .envファイルから環境変数を読み込む

class BookGenerator:
    def __init__(self, syllabus_file):
        self.syllabus_file = syllabus_file
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")  # 環境変数からAPI keyを取得
        )

    def generate_book(self):
        with open(self.syllabus_file, "r") as f:
            syllabus = yaml.safe_load(f)

        if not os.path.exists("ais"):
            os.makedirs("ais")

        self._save_ai_docs()

        for chapter in tqdm(syllabus, desc="Generating chapters"):
            if "chapter" in chapter:
                chapter_dir = f"book/chapter{chapter['chapter']}"
                os.makedirs(chapter_dir, exist_ok=True)

                topics = chapter["topics"]
                description = chapter["description"]

                markdown_file = f"{chapter_dir}/chapter{chapter['chapter']}.md"
                with open(markdown_file, "w") as f:
                    f.write(f"# Chapter {chapter['chapter']}\n\n")
                    f.write(f"## Topics\n")
                    for topic in topics:
                        f.write(f"- {topic}\n")
                    f.write(f"\n## Description\n{description}\n\n")

                    lecture_content = self._generate_lecture_content(chapter["topics"], description)
                    f.write(f"## Lecture Content\n{lecture_content}\n\n")

                    quiz_content = self._generate_quiz_content(chapter["topics"], description)
                    f.write(f"## Quiz Content\n{quiz_content}\n")

        print("Book generation completed!")

    def _save_ai_docs(self):
        ai_docs = {
            "講義資料生成AI": "lecture_generator.md",
            "問題生成AI": "quiz_generator.md"
        }

        for title, filename in ai_docs.items():
            with open(f"ais/{filename}", "w") as f:
                f.write(f"## {title}\n\n")
                start_index = self.syllabus_file.find(f"## {title}")
                end_index = self.syllabus_file.find("##", start_index + 1)
                if end_index == -1:
                    end_index = len(self.syllabus_file)
                ai_doc = self.syllabus_file[start_index:end_index].strip()
                f.write(ai_doc)

    def _generate_lecture_content(self, topics, description):
        with open("ais/lecture_generator.md", "r") as f:
            lecture_content_prompt = f.read().format(lecture_title=", ".join(topics), lecture_description=description)

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
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

        return response.content[0].text.strip()

    def _generate_quiz_content(self, topics, description):
        with open("ais/quiz_generator.md", "r") as f:
            quiz_content_prompt = f.read().format(lecture_title=", ".join(topics), lecture_description=description)

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
            messages=[
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

        return response.content[0].text.strip()


if __name__ == "__main__":
    generator = BookGenerator("syllabus.yaml")
    generator.generate_book()
