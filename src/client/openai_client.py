import json
import os

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice


class OpenAIClient:
    env_var_api_key = "OPENAI_API_KEY"
    env_var_org_key = "OPENAI_ORG_ID"

    def _load_assessment_clause(self):
        with open("public/assessment.txt", "r") as file:
            text = file.read()
            return text

    def __init__(self):
        api_key = os.environ[self.env_var_api_key]
        organization = os.environ[self.env_var_org_key]
        self.client = OpenAI(api_key=api_key, organization=organization)
        self.assessment_clause = self._load_assessment_clause()

    def get_reply(self, messages: list[dict]) -> str:
        response: ChatCompletion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=messages,
        )
        response: Choice = response.choices[0]
        response: ChatCompletionMessage = response.message
        return response.content

    def get_assessment_reply(
        self, title: str, images: list[str], description: str
    ) -> dict:
        title = "<title>" + title + "<title>"
        images = "<image>" + str(images) + "<image>"
        description = "<description>" + description + "<description>"
        reply = self.get_reply(
            [
                {
                    "role": "system",
                    "content": self.assessment_clause,
                },
                {"role": "user", "content": title + "\n" + images + "\n" + description},
            ]
        )
        return json.loads(reply)


if __name__ == "__main__":

    def return_test_text():
        with open("keys/test.txt", "r") as file:
            text = file.read()
            return text

    AIClient = OpenAIClient()
    print(
        AIClient.get_assessment_reply(
            title="Portable Laptop wooden Table",
            images=[
                "iPhone on a wooden table",
                "a group of smoke stacks with smoke coming out of them",
            ],
            description="Latest iPhone runs instead of A17 Bionic Chip",
        )
    )
