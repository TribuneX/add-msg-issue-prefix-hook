#!/usr/bin/env python3

import argparse
import sys
import re
import subprocess


def get_ticket_id_from_branch_name(branch):
    matches = re.findall('[a-zA-Z0-9]{1,10}-[0-9]{1,5}', branch)
    if len(matches) > 0:
        return matches[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    parser.add_argument(
        '-t', '--template', default="[{}]",
        help='Template to render ticket id into',
    )
    args = parser.parse_args()
    commit_msg_filepath = args.commit_msg_filepath
    template = args.template

    branch = ""
    try:
        branch = subprocess.check_output(["git","symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
    except Exception as e:
        print(e)

    result = get_ticket_id_from_branch_name(branch)
    issue_number = ""

    if result:
        issue_number = result.upper()

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        # f.seek(0, 0)
        new_content = add_issue_number_to_scope(content, issue_number)
        f.write(new_content)


def add_issue_number_as_prefix(content, issue_number, template):
    content_subject = content.split("\n", maxsplit=1)[0].strip()
    if issue_number and issue_number not in content_subject:
        prefix = template.format(issue_number)
        return "{} {}".format(prefix, content)
    else:
        return content


def add_issue_number_to_scope(commit_message, issue_number):
    if issue_number and issue_number in commit_message:
        return commit_message

    pattern = r'^(?P<type>[\w-]+)(\((?P<scope>[\w-]+)\))?!?: (?P<description>.+)$'
    match = re.match(pattern, commit_message)
    if match:
        commit_type = match.group('type')
        if match.group('scope'):
            commit_scope = match.group('scope') + f', {issue_number}'
        else:
            commit_scope = issue_number
        commit_description = match.group('description')
    else:
        raise ValueError('Invalid commit message format')

    return f'{commit_type}({commit_scope}): {commit_description}'


if __name__ == "__main__":
    exit(main())
