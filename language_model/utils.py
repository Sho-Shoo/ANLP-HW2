def get_in_context_example() -> str:
    questions, answers = [], []

    with open("data/train/questions.txt", "r") as f:
        while True:
            line = f.readline().strip()
            if not line: break
            questions.append(line)

    with open("data/train/reference_answers.txt", "r") as f:
        while True:
            line = f.readline().strip()
            if not line: break
            answers.append(line)

    if len(questions) != len(answers):
        raise RuntimeError("In context QA pair count mismatch.")

    examples = []
    for q, a in zip(questions, answers):
        example = f"Q: {q}\nA: {a}"
        examples.append(example)

    examples = "\n\n".join(examples)

    return examples.strip()


if __name__ == "__main__":
    print(get_in_context_example())
