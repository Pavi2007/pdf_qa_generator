from transformers import pipeline, AutoTokenizer
import re


class QuestionGenerator:
    def __init__(self, model_name="google/flan-t5-base"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.generator = pipeline(
            "text2text-generation",
            model=model_name,
            tokenizer=self.tokenizer
        )

        # Determine a safe token window for chunks (reserve tokens for the prompt/generation)
        model_max = getattr(self.tokenizer, "model_max_length", 512)
        self.safe_tokens = max(64, model_max - 128)

    def clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def chunk_text(self, text):
        # Token-aware chunking to avoid exceeding model max length
        token_ids = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        i = 0
        while i < len(token_ids):
            seg = token_ids[i:i + self.safe_tokens]
            chunk = self.tokenizer.decode(seg, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            chunks.append(chunk)
            i += self.safe_tokens
        return chunks

    def generate_questions(self, text):
        cleaned = self.clean_text(text)
        chunks = self.chunk_text(cleaned)

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