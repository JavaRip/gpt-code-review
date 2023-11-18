import requests
import argparse
import os
from openai import OpenAI

OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
TOKEN = os.environ.get('GH_TOKEN')
PROMPT = os.environ.get('PROMPT', 'Give a code review in the style of Gordan Ramsay, be harsh cruel and critically, to a comedic and extreme level.')
PR_NUMBER = os.environ.get('PR_NUMBER')
REPO = os.environ.get('REPO')
DELIM = '||||||||||||||||||'

def prep_for_gpt(diff):
    # Check if the diff is longer than 4000 characters
    if len(diff) > 4000:
        # Split the diff using the provided delimiter
        split_diffs = diff.split(DELIM)

        # Filter out parts that are too long
        filtered_diffs = [part for part in split_diffs if len(part) <= 4000]

        # Optionally, print a warning if any parts were removed
        if len(filtered_diffs) < len(split_diffs):
            print('WARNING: Some items in diff were too long and have been removed')

        return filtered_diffs
    else:
        return [diff]


def get_gpt_response(prompt_body_array):
  client = OpenAI(api_key=OPEN_API_KEY)
  answers = []
  for body in prompt_body_array:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": body}
        ]
    )
    answers.append(completion.choices[0].message.content)

  return answers

def remove_ignored(diff, ignored):
    ret_array = []
    diff_array = diff.split('diff --git')

    for diff in diff_array:
        ignore_diff = False
        for ignore in ignored:
            if ignore in diff:
                ignore_diff = True
        if not ignore_diff:
            ret_array.append(diff)

    return DELIM.join(ret_array)

def post_comment_to_pr(repo, pr_number, comment):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": comment
    }

    response = requests.post(url, json=data, headers=headers)
    return response

def get_diff(repo, pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def main(pr_number, repo):
    print('=============== MAIN =================')
    print(f'pr_number: {pr_number}')
    print(f'repo: {repo}')

    diff = get_diff(repo, pr_number)
    filtered_diff = remove_ignored(diff, ['Pipfile.lock'])
    prompts = prep_for_gpt(filtered_diff)
    answers = get_gpt_response(prompts) # get from chatblt

    comment = '\n'.join(answers)
    print('================================')
    print(comment)
    print('================================')
    post_comment_to_pr(
      repo,
      pr_number,
      comment,
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(
      PR_NUMBER,
      REPO,
    )