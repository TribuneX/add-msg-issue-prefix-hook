import pytest

from add_msg_issue_prefix_hook.add_msg_issue_prefix import add_issue_number_as_prefix, \
    add_issue_number_to_scope


def test_add_issue_number_as_prefix():
    new_content = add_issue_number_as_prefix("initial commit", "PRE-10", "[{}]")

    assert new_content == "[PRE-10] initial commit"


def test_add_issue_number_in_simple_conventional_commit():
    new_content = add_issue_number_to_scope("chore: initial commit", "PRE-10")

    assert new_content == "chore(PRE-10): initial commit"


# def test_empty_scope_is_not_allowed():
#     new_content = append_scope_to_commit("chore(): initial commit", "PRE-10")
#
#     assert new_content == "chore(PRE-10): initial commit"


def test_not_add_issue_number_in_conventional_commit_if_it_already_exists():
    new_content = add_issue_number_to_scope("chore(PRE-10): initial commit", "PRE-10")

    assert new_content == "chore(PRE-10): initial commit"


def test_add_issue_number_as_additional_scope_in_conventional_commit():
    new_content = add_issue_number_to_scope("chore(deps): initial commit", "PRE-10")

    assert new_content == "chore(deps, PRE-10): initial commit"
