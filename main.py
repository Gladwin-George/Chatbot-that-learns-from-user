import json
from difflib import get_close_matches

# Load the JSON data
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Save the user data
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the best match
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    # Convert all questions to lowercase for case-insensitive matching
    user_question_lower = user_question.lower()
    questions_lower = [q.lower() for q in questions]

    matches: list[str] = get_close_matches(user_question_lower, questions_lower, n=2, cutoff=0.6)
    return matches[0] if matches else None

# Answer for the question
def answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]

# Main function
def chatbot():
    knowledge_base = load_knowledge_base("knowledge_base.json")

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "exit":
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")

        else:
            print("Bot: Sorry, I don't understand. Can you teach me?")

            new_answer = input("Type your answer or 'exit' to skip: ")

            if new_answer.lower() != "exit":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("Bot: Thank you, I will remember that.")

if __name__ == "__main__":
    chatbot()
