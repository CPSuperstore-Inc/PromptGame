with open("PromptGame/files/illegalAnswers.txt") as f:
    ILLEGAL_ANSWERS = [i.lower().replace("\n", "") for i in f.readlines()]


def is_answer_legal(text:str):
    return text.lower() not in ILLEGAL_ANSWERS