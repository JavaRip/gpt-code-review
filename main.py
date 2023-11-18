import requests
import argparse
import os
from openai import OpenAI

OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
TOKEN = os.environ.get('GH_TOKEN')
PROMPT = os.environ.get('PROMPT', 'You are a expert developer. Bless us with your knowledge and critique. Be gentle but firm as strength comes with thick skin.')
DELIM = os.environ.get('DELIM')

def prep_for_gpt(diff):
    # Check if the diff is longer than 4000 characters
    if len(diff) > 4000:
        # Split the diff using the provided delimiter
        split_diffs = diff.split(DELIM)

        # Check each split part's length
        for part in split_diffs:
            if len(part) > 4000:
                print('WARNING: ITEM IN DIFF TOO LONG')

        return split_diffs
    else:
        return [diff]

def get_gpt_response(prompt_body_array):
  client = OpenAI()
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

def get_diff(repo, src, dest, pr_number):
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

def main(pr_number, src, dest, repo):
    print('=============== MAIN =================')
    print(f'pr_number: {pr_number}')
    print(f'src_commit_id: {src}')
    print(f'dest_commit_id: {dest}')
    print(f'repo: {repo}')

    diff = get_diff(repo, src, dest, pr_number)
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

    parser.add_argument(
      'src',
      type=str,
      help='the commit or branch the merge is coming from',
    )

    parser.add_argument(
      'dest',
      type=str,
      help='the commit or branch the merge is coming into',
    )

    parser.add_argument(
      'pr',
      type=str,
      help='the pr number to append the output to as a comment',
    )

    parser.add_argument(
      'repo',
      type=str,
      help='the repo to run the script on',
    )

    args = parser.parse_args()
    main(
      args.pr,
      args.src,
      args.dest,
      args.repo,
    )
