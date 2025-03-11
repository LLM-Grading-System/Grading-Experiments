import json
import os

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
    general_score: int = Field(description="General score of student code, from 0 to 5")


with open("experiments/exp2/system.md", encoding="utf-8") as f:
    system_prompt = f.read()

with open("experiments/exp2/task_wrong_solution.md", encoding="utf-8") as f:
    right_solution = f.read()

criteria_code_prompt = ChatPromptTemplate(
    [
        (
            "system",
            system_prompt.replace("{", "{{").replace("}", "}}")
        ),
        (
            "human",
            "{input}"
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

result: CriteriaFeedback = chain.invoke(right_solution)
print("Feedback: ", result.general_feedback)
print("Score: ", result.general_score)
score = sum(item.is_met for item in result.criteria) / len(result.criteria)
print("Criteria based score:", round(score, 2))

with open("experiments/exp2/result.json", mode="w", encoding="utf-8") as f:
    json.dump(result.model_dump(), f)
