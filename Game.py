import os
import csv
import random
from typing import List, Dict

class Quiz:
    EXPECTED_COLUMNS = ["question", "correct_answer", "incorrect_answer_1", "incorrect_answer_2", "incorrect_answer_3"]

    def __init__(self, file_path: str):
        """Initializes the quiz by loading questions from the specified file."""
        self.questions = self.load_questions(file_path)

    def load_questions(self, file_path: str) -> List[Dict[str, str]]:
        """Loads questions from a CSV file and returns a list of questions with shuffled options."""
        questions = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                if not set(self.EXPECTED_COLUMNS).issubset(reader.fieldnames):
                    raise ValueError("Error: faltan columnas esperadas en el archivo CSV.")
                
                for row in reader:
                    options = [opt for opt in [row.get("correct_answer"), row.get("incorrect_answer_1"), 
                                               row.get("incorrect_answer_2"), row.get("incorrect_answer_3")] if opt]
                    random.shuffle(options)
                    questions.append({
                        "question": row.get("question", "Question not available"),
                        "options": options,
                        "correct_answer": row.get("correct_answer", "")
                    })
        except FileNotFoundError:
            print("Error: Archivo no encontrado. Por favor verifique la ruta del archivo.")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Error inesperado: {e}")
        return questions

    def get_user_answer(self, num_options: int) -> int:
        """Gets a valid answer from the user and returns it as an index."""
        while True:
            try:
                answer = int(input("Selecciona el número de tu respuesta: "))
                if 1 <= answer <= num_options:
                    return answer - 1
                else:
                    print("Por favor digita un número válido.")
            except ValueError:
                print("Entrada no válida. Por favor ingresa un número.")

    def run_quiz(self):
        """Runs the quiz, displaying questions, options, and calculating the final score."""
        if not self.questions:
            print("No hay preguntas cargadas. Saliendo del cuestionario.")
            return

        score = 0
        random.shuffle(self.questions)  # Optional: shuffle the order of questions
        total_questions = len(self.questions)

        for i, question in enumerate(self.questions):
            print(f"\nQuestion {i + 1}/{total_questions}: {question['question']}")
            for idx, option in enumerate(question["options"], start=1):
                print(f"{idx}. {option}")

            user_answer_idx = self.get_user_answer(len(question["options"]))
            if question["options"][user_answer_idx] == question["correct_answer"]:
                print("¡Correcto!")
                score += 1
            else:
                print(f"Incorrecto. La respuesta correcta era: {question['correct_answer']}")

        print(f"\n¡Quiz completedo! Tu puntaje final es de {score}/{total_questions}.")

# Define the path to the questions file
questions_file = os.path.expanduser("~/Desktop/Questions_gameCo/questionsCo.csv")

# Run the program
quiz = Quiz(questions_file)
quiz.run_quiz()
2