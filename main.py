import requests
import argparse
import os

OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
TOKEN = os.environ.get('GITHUB_TOKEN')

def post_comment_to_pr(repo, pr_number, comment):
    print('============ POSTING COMMENT TO PR ============')
    print(f'repo: {repo}')
    print(f'pr_number: {pr_number}')
    print(f'comment: {comment}')

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

def main(pr_number, src, dest, repo):
    print(f'pr_number: {pr_number}')
    print(f'src_commit_id: {src}')
    print(f'dest_commit_id: {dest}')
    print(f'repo: {repo}')

    post_comment_to_pr(
      repo,
      pr_number,
      f'pr_number: {pr_number}\nsrc_commit_id: {src}\ndest_commit_id: {dest}\nrepo: {repo}',
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
