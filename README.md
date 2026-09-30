# Interactive Python Quiz Engine

## Overview
**Interactive Python Quiz Engine** is an object-oriented Python application designed to load, manage, and execute interactive quizzes from JSON configuration files or programmatically created questions. It provides an efficient solution for conducting command-line quizzes with automated answer checking, flexible formatting, answer explanations, and detailed scoring summaries.

## Features
- **JSON Quiz Storage**: Save and load quiz questions and metadata to and from JSON files.
- **Flexible Question Structure**: Support for question prompts, multiple-choice options, correct answers, and detailed explanations.
- **Case-Insensitive Answer Verification**: Normalizes single-character and full-string answers for accurate evaluation.
- **Interactive Console Quiz Runner**: Interactive CLI runner displaying questions, multiple-choice options, scoring, and post-question explanations.
- **Custom Input/Output Injection**: Supports dependency injection for input and print callbacks, facilitating unit testing and programmatical execution.
- **Detailed Score Reporting**: Displays total score, percentage, and returns summary data upon quiz completion.
- **Automated Test Suite**: Unit test suite verifying model creation, JSON serialization, and execution mechanics.

## Technologies Used
- **Python 3**: Primary programming language.
- **Python Standard Library**: `json`, `os`, `typing`, `unittest`, `tempfile`.
- **pytest**: Test runner for executing unit tests.

## How It Works
1. **Question Initialization**: The `Question` class encapsulates the question prompt, answer, optional options list, and optional explanation.
2. **Quiz Aggregation**: The `Quiz` class holds a list of `Question` instances along with a quiz title.
3. **JSON Loading/Saving**: The quiz reads or writes JSON files using `Quiz.load_from_json()` and `Quiz.save_to_json()`, deserializing JSON structure into `Question` objects via `Question.from_dict()`.
4. **Execution Flow**: When `quiz.run()` is invoked:
   - Iterates through each question in order.
   - Displays prompt and options (if available).
   - Captures user input and checks correctness via `question.is_correct()`.
   - Displays feedback (Correct/Incorrect) and prints the explanation if present.
   - Computes score and percentage, returning a dictionary containing execution details.

## Installation and Setup

### Prerequisites
- Python 3.8 or higher installed on your system.

### Setup Instructions
1. **Clone or download the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies (optional for running tests)**:
   ```bash
   pip install pytest
   ```

## How to Run

### Running the Quiz Application
Execute the main script directly using Python:
```bash
python3 quiz.py
```
By default, `quiz.py` checks for `sample_quiz.json` in the current working directory and executes it.

### Running Unit Tests
To run the automated unit test suite:
```bash
PYTHONPATH=. pytest
```
Alternatively, using standard library `unittest`:
```bash
python3 -m unittest test_quiz.py
```

## Project Structure
```
.
├── quiz.py           # Core quiz engine (Question, Quiz classes, and CLI runner)
├── sample_quiz.json  # Sample JSON file containing general knowledge questions
└── test_quiz.py      # Unit test suite for question logic, quiz storage, and runner
```

- **`quiz.py`**: Contains `Question` and `Quiz` classes along with serialization and CLI execution logic.
- **`sample_quiz.json`**: Pre-configured JSON data file with questions, multiple-choice options, answers, and explanations.
- **`test_quiz.py`**: Automated unit tests using `unittest`.

## Usage

### 1. Using Pre-configured JSON Quiz Files
Create a JSON file structured as follows:
```json
{
  "title": "My Custom Quiz",
  "questions": [
    {
      "prompt": "What is the capital of France?",
      "options": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
      "answer": "C",
      "explanation": "Paris is the capital of France."
    }
  ]
}
```

Load and run it programmatically in Python:
```python
from quiz import Quiz

quiz = Quiz.load_from_json("sample_quiz.json")
quiz.run()
```

### 2. Creating Quizzes Programmatically
```python
from quiz import Question, Quiz

quiz = Quiz("Math Quiz")
quiz.add_question(
    Question(
        prompt="What is 2 + 2?",
        options=["A. 3", "B. 4", "C. 5"],
        answer="B",
        explanation="2 + 2 equals 4."
    )
)

# Run quiz
results = quiz.run()

# Save quiz to JSON
quiz.save_to_json("my_quiz.json")
```

## Future Enhancements
- Support for multiple-choice question shuffling or randomizing question order.
- Time limit enforcement per question or quiz session.
- Graphical user interface (GUI) or web interface integration.
- Analytics for tracking historical quiz scores over time.

## Conclusion
The **Interactive Python Quiz Engine** is a lightweight, robust, and easily extensible Python library and CLI tool for running JSON-driven quizzes. With strong test coverage and standard library dependency minimalization, it provides a reliable foundation for interactive assessment applications.
