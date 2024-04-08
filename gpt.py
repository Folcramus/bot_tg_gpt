import httpx
import time
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
assistant_id = os.getenv("ASSISTANT_ID")
proxy = httpx.Proxy(url=os.getenv("IP"), auth=(os.getenv("LOGIN"), os.getenv("PASS")))
client = OpenAI(api_key=os.getenv("API_KEY"),
                http_client=httpx.Client(proxy=proxy, timeout=6000))


def create_thread(ass_id, prompt):
    thread = client.beta.threads.create()
    my_thread_id = thread.id
    message = client.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=ass_id,
    )
    return run.id, thread.id


def check_status(run_id, thread_id):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )

    return run.status

"""Обработка обычных сообщений"""
def messaging(mess: str) -> str:
    my_run_id, my_thread_id = create_thread(assistant_id, mess)
    status = check_status(my_run_id, my_thread_id)
    while status != "completed":
        status = check_status(my_run_id, my_thread_id)
        time.sleep(2)
    response = client.beta.threads.messages.list(
        thread_id=my_thread_id
    )
    if response.data:
        return response.data[0].content[0].text.value

"""Обработка структурированных сообщений"""
def command_gpt(content: str) -> str:
    mess  = "Структурируй содержание  данного  сообщения по красоте: " + content
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": mess,
            }
        ],
        model="gpt-4-turbo-preview",
    )
    return chat_completion.choices[0].message.content