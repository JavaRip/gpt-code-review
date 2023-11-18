import argparse

def main(pr_number, src_commit_id, dest_commit_id):
    print(f'pr_number: {pr_number}')
    print(f'src_commit_id: {src_commit_id}')
    print(f'dest_commit_id: {dest_commit_id}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
	'source-commit-id',
	type=str,
	help='the commit the merge is coming from',
    )

    parser.add_argument(
	'dest-commit-id',
	type=str,
	help='the commit the merge is coming into',
    )

    parser.add_argument(
	'pr-number',
	type=str,
	help='the pr number',
    )

    args = parser.parse_args()
    main(args.commit_id)
