import unittest
import os
import tempfile
from quiz import Question, Quiz


class TestQuestion(unittest.TestCase):
    def test_question_creation(self):
        q = Question("What is 2+2?", "4", ["A. 2", "B. 4"], "2+2=4")
        self.assertEqual(q.prompt, "What is 2+2?")
        self.assertEqual(q.answer, "4")
        self.assertEqual(len(q.options), 2)
        self.assertEqual(q.explanation, "2+2=4")

    def test_is_correct(self):
        q = Question("Select A", "A", ["A. Yes", "B. No"])
        self.assertTrue(q.is_correct("a"))
        self.assertTrue(q.is_correct("A "))
        self.assertFalse(q.is_correct("B"))

    def test_to_dict_and_from_dict(self):
        q = Question("Prompt", "Ans", ["Opt1"], "Exp")
        d = q.to_dict()
        q2 = Question.from_dict(d)
        self.assertEqual(q2.prompt, q.prompt)
        self.assertEqual(q2.answer, q.answer)
        self.assertEqual(q2.options, q.options)
        self.assertEqual(q2.explanation, q.explanation)


class TestQuiz(unittest.TestCase):
    def test_add_question(self):
        quiz = Quiz("Test Quiz")
        q = Question("Q1", "A")
        quiz.add_question(q)
        self.assertEqual(len(quiz.questions), 1)

    def test_save_and_load_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_quiz.json")
            quiz = Quiz("Saved Quiz")
            quiz.add_question(Question("Q1?", "A", ["A. 1", "B. 2"], "Exp1"))
            quiz.save_to_json(filepath)

            loaded_quiz = Quiz.load_from_json(filepath)
            self.assertEqual(loaded_quiz.title, "Saved Quiz")
            self.assertEqual(len(loaded_quiz.questions), 1)
            self.assertEqual(loaded_quiz.questions[0].prompt, "Q1?")

    def test_quiz_run(self):
        quiz = Quiz("Run Quiz")
        quiz.add_question(Question("Q1?", "A", ["A. 1", "B. 2"]))
        quiz.add_question(Question("Q2?", "B", ["A. 1", "B. 2"]))

        answers = ["a", "a"]  # Q1 correct, Q2 incorrect
        answers_iter = iter(answers)

        output_logs = []

        def mock_input(prompt):
            return next(answers_iter)

        def mock_print(msg):
            output_logs.append(msg)

        results = quiz.run(input_func=mock_input, print_func=mock_print)

        self.assertEqual(results["score"], 1)
        self.assertEqual(results["total"], 2)
        self.assertEqual(results["percentage"], 50.0)


if __name__ == "__main__":
    unittest.main()
