import os
import platform
import re
import argparse

import requests

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.chains import ChatVectorDBChain
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI

parser = argparse.ArgumentParser()
parser.add_argument('--openai_api_key', help='Your OpenAI API Key')
parser.add_argument('--github_token', help='Your Github Token')
parser.add_argument('--github_pr_id', help='Your Github PR ID')
parser.add_argument('--openai_model', default="gpt-3.5-turbo",
                    help='GPT model to use. Options: gpt-3.5-turbo, text-davinci-002, text-babbage-001, text-curie-001, text-ada-001')
parser.add_argument('--openai_temperature', default=0.7,
                    help='Sampling temperature to use. Higher values means the model will take more risks')
parser.add_argument('--openai_top_p', default=0.8,
                    help='An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.')
args = parser.parse_args()

top_p = float(args.openai_top_p)
temperature = float(args.openai_temperature)
model = args.openai_model
pr_id = args.github_pr_id
gh_token = args.github_token

repository = os.getenv('GITHUB_REPOSITORY')
os.environ["OPENAI_API_KEY"] = args.openai_api_key

print('Python: ', platform.python_version())


def get_pull_request_diff():
    url = f"https://api.github.com/repos/{repository}/pulls/{pr_id}"
    print(url)

    headers = {
        'Authorization': f"token {gh_token}",
        'Accept': 'application/vnd.github.v3.diff'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.text

def add_review_comments(comments: list):
    url = f"https://api.github.com/repos/{repository}/pulls/{pr_id}/reviews"

    headers = {
        'Authorization': f"token {gh_token}",
        'X-GitHub-Api-Version': "2022-11-28"
    }
    data = {
        'body': f"This is Auto Review by {model}",
        'event': "COMMENT",
        'comments': comments,
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.text


def get_plain_text_document(text: str):
    metadata = {"source": "unknown"}
    return [Document(page_content=text, metadata=metadata)]


def get_filenames_from_diff(diff_text: str):
    # diff --git 뒤의 filename 부분을 가져오기 위한 정규식
    pattern = r'diff --git\s+a/(.*?)\s+'
    matches = re.findall(pattern, diff_text)
    return matches


if __name__ == '__main__':
    diff = get_pull_request_diff()

    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    diff_doc = text_splitter.split_documents(get_plain_text_document(diff))

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(diff_doc, embeddings)

    top_k = min(len(diff_doc), 4)
    diff_qa = ChatVectorDBChain.from_llm(
        ChatOpenAI(temperature=temperature, top_p=top_p, model=model),
        vectordb,
        return_source_documents=True, top_k_docs_for_context=top_k)

    filenames = get_filenames_from_diff(diff)

    reviews = []
    for file in filenames:
        title_query = f"""
        Please summarize the changes to file {file} in one line.
        """
        review_query = f"""
        As a code reviewer, please review the {file} file and tell us where it could be improved based on the diff.
        """

        title_result = diff_qa({"question": title_query, "chat_history": []})
        review_result = diff_qa({"question": review_query, "chat_history": []})

        title_answer = title_result["answer"]
        title_source = title_result["source_documents"]

        review_answer = review_result["answer"]
        review_source = review_result["source_documents"]

        print(f"Review File: {file}")

        print(f"summary:{title_answer}")
        # print(f"summary source:{title_source}")

        print(f"detail:{review_answer}")
        # print(f"detail source:{review_source}")

        reviews.append(
            {"path": file, "body": f"### Review\n{title_answer}\n\n**Detail**\n{review_answer}",
             "position": 1})

    add_review_comments(reviews)
