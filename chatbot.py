import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    """Loads knowledge base data from a JSON file."""
    with open('knowledge_base.json', 'r', encoding="utf-8") as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    """Saves knowledge base data to a JSON file."""
    with open('knowledge_base.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """Finds the closest match to a user question from a list of questions."""
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """Retrieves the answer for a specific question from the knowledge base."""
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


def chat_bot():
    """Main function for the chat bot."""
    # Load knowledge base
    knowledge_base = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break
        # import pdb; pdb.set_trace() 
        # Find best match
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(answer)
        else:
            print("Bot: I don't know, can you teach me? ")
            new_answer: str = input("Type the answer or 'leave' to leave: ")

            if new_answer.lower() != 'leave':
                knowledge_base["questions"].append({'question': user_input, 'answer': new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thanks man! I have learned something new!")


if __name__ == '__main__':
    chat_bot()
