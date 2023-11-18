import argparse

def main(pr_number, src_commit_id, dest_commit_id):
    print(f'pr_number: {pr_number}')
    print(f'src_commit_id: {src_commit_id}')
    print(f'dest_commit_id: {dest_commit_id}')


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

    args = parser.parse_args()
    main(args.commit_id)
