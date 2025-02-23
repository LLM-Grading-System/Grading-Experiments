import json
import os
import time

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
MODEL = os.environ["MISTRAL_MODEL"]
API_KEY = os.environ["MISTRAL_API_KEY"]


class CriteriaNote(BaseModel):
    name: str = Field(description="The essence of the criterion")
    problem: str = Field(default="", description="What is the problem with the code according to the criterion")
    is_met: bool = Field(description="If the code meets the criteria, return True, otherwise False")


class CriteriaFeedback(BaseModel):
    criteria: list[CriteriaNote] = Field(default=[])
    general_feedback: str = Field(description="General feedback about the code according to the criteria for student")


with open("experiments/exp1/task.md", encoding="utf-8") as f:
    task_description = f.read()

with open("experiments/exp1/task_wrong_solution.md", encoding="utf-8") as f:
    wrong_solution = f.read()

with open("experiments/exp1/task_right_solution.md", encoding="utf-8") as f:
    right_solution = f.read()

criteria_code_prompt = ChatPromptTemplate(
    [
        (
            "system",
            "Ты помощник преподавателя для проверки практических заданий по программированию. \n" + task_description
        ),
        (
            "human",
            "Код студента: \n {solution}"
        ),
    ]
)


model = ChatMistralAI(
    model=MODEL,
    mistral_api_key=API_KEY,
    temperature=0,
)


model_with_structured_output = model.with_structured_output(CriteriaFeedback)
chain = criteria_code_prompt | model_with_structured_output

for solution, solution_type in zip([wrong_solution, right_solution], ["wrong", "right"]):
    result: CriteriaFeedback = chain.invoke({"solution": solution})

    output_file = f"experiments/exp1/task_{solution_type}_solution_feedback.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f)

    print("Type:", solution_type)
    print("Feedback: ", result.general_feedback)
    score = sum(item.is_met for item in result.criteria) / len(result.criteria)
    print("Score:", round(score, 2))
    time.sleep(1)