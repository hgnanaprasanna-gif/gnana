import json
import os
from typing import List, Dict, Any, Optional, Callable


class Question:
    """Represents an individual quiz question."""

    def __init__(
        self,
        prompt: str,
        answer: str,
        options: Optional[List[str]] = None,
        explanation: Optional[str] = None,
    ):
        self.prompt = prompt
        self.options = options or []
        self.answer = answer.strip().upper() if len(answer.strip()) == 1 else answer.strip()
        self.explanation = explanation

    def is_correct(self, user_answer: str) -> bool:
        """Checks if user's answer matches the correct answer (case-insensitive)."""
        clean_user = user_answer.strip().upper() if len(user_answer.strip()) == 1 else user_answer.strip()
        return clean_user.lower() == self.answer.lower()

    def to_dict(self) -> Dict[str, Any]:
        """Converts question object to a dictionary."""
        data = {
            "prompt": self.prompt,
            "answer": self.answer,
        }
        if self.options:
            data["options"] = self.options
        if self.explanation:
            data["explanation"] = self.explanation
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        """Creates a Question instance from a dictionary."""
        return cls(
            prompt=data["prompt"],
            answer=str(data["answer"]),
            options=data.get("options"),
            explanation=data.get("explanation"),
        )


class Quiz:
    """Manages a collection of questions and conducts the quiz."""

    def __init__(self, title: str = "Quiz"):
        self.title = title
        self.questions: List[Question] = []

    def add_question(self, question: Question) -> None:
        """Adds a Question object to the quiz."""
        self.questions.append(question)

    @classmethod
    def load_from_json(cls, filepath: str) -> "Quiz":
        """Loads a quiz from a JSON file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        quiz = cls(title=data.get("title", "Quiz"))
        for q_data in data.get("questions", []):
            quiz.add_question(Question.from_dict(q_data))
        return quiz

    def save_to_json(self, filepath: str) -> None:
        """Saves the quiz to a JSON file."""
        data = {
            "title": self.title,
            "questions": [q.to_dict() for q in self.questions],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def run(
        self,
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print,
    ) -> Dict[str, Any]:
        """
        Executes the quiz interactively or programmatically.
        Returns a dictionary summary of results.
        """
        score = 0
        total = len(self.questions)

        print_func(f"=== {self.title} ===")
        print_func(f"Total Questions: {total}\n")

        results = []

        for idx, q in enumerate(self.questions, start=1):
            print_func(f"Question {idx}: {q.prompt}")
            if q.options:
                for option in q.options:
                    print_func(f"  {option}")

            user_ans = input_func("Your answer: ")
            correct = q.is_correct(user_ans)

            if correct:
                score += 1
                print_func(" Correct!\n")
            else:
                print_func(f" Incorrect. The correct answer was: {q.answer}\n")

            if q.explanation:
                print_func(f"Explanation: {q.explanation}\n")

            results.append({
                "question": q.prompt,
                "user_answer": user_ans,
                "correct_answer": q.answer,
                "is_correct": correct,
            })

        percentage = (score / total * 100) if total > 0 else 0
        print_func("=== Quiz Completed ===")
        print_func(f"Your Score: {score}/{total} ({percentage:.1f}%)\n")

        return {
            "title": self.title,
            "score": score,
            "total": total,
            "percentage": percentage,
            "details": results,
        }


def main():
    json_path = "sample_quiz.json"
    if os.path.exists(json_path):
        quiz = Quiz.load_from_json(json_path)
    else:
        quiz = Quiz("Sample Quiz")
        quiz.add_question(
            Question(
                prompt="What is 1 + 1?",
                options=["A. 1", "B. 2", "C. 3"],
                answer="B",
                explanation="1 + 1 equals 2.",
            )
        )

    quiz.run()


if __name__ == "__main__":
    main()
