from transformers import pipeline
import re

class QuestionGenerator:
    def __init__(self):
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base"
        )

    def clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def chunk_text(self, text, chunk_size=500):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i:i+chunk_size]))
        return chunks

    def generate_questions(self, text):

        cleaned = self.clean_text(text)
        chunks = self.chunk_text(cleaned, chunk_size=500)

        all_questions = []
        seen_questions = set()
        question_number = 1

        for chunk in chunks:

            prompt = f"""
Generate 5 clear university-level short-answer questions 
from the following academic content.

Rules:
- Ask definition questions if definitions exist.
- Ask explanation questions if concepts are described.
- Ask list/type questions if categories exist.
- Only output questions.
- Do not repeat questions.
- Keep questions complete and meaningful.

Content:
{chunk}
"""

            output = self.generator(
                prompt,
                max_length=256,
                do_sample=False
            )[0]["generated_text"]

            questions = output.split("\n")

            for q in questions:
                q = q.strip()

                if len(q) > 15 and q not in seen_questions:
                    seen_questions.add(q)
                    all_questions.append(f"{question_number}. {q}")
                    question_number += 1

            if len(all_questions) >= 30:
                break

        return "\n".join(all_questions[:30])