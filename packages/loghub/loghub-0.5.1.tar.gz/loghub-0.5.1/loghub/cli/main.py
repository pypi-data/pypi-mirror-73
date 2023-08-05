# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Build a list of issues and pull requests per Github milestone."""

# yapf: disable

from __future__ import print_function

# Standard library imports
import argparse
import sys
import textwrap

# Local imports
from loghub.cli.common import add_common_parser_args, parse_password_check_repo
from loghub.core.config import load_config
from loghub.core.formatter import create_changelog

# yapf: enable

PY2 = sys.version[0] == '2'


def check_github_deprecation(username='', password=''):
    """
    Inform users that username and password are deprecated by Github API.
    """
    text = (
        'Deprecation Notice: GitHub will discontinue password '
        'authentication to the API. You must now authenticate '
        'to the GitHub API with an API token, such as an OAuth '
        'access token, GitHub App installation access token, or '
        'personal access token, depending on what you need to do '
        'with the token. Password authentication to the API will be '
        'removed on November 13, 2020. For more information, including '
        'scheduled brownouts, see: '
        'https://developer.github.com/changes/'
        '2020-02-14-deprecating-password-auth/         '
        'To create a new token go to: https://github.com/settings/tokens'
    )
    if username or password:
        print('\n' + '\n'.join(textwrap.wrap(text, 79)) + '\n')


def main():
    """Main script."""
    parse_arguments(skip=False)


def create_label_groups(groups):
    """Create info dictionaries for label groups."""
    group_dicts = []
    if groups:
        for item in groups:
            dic = {}
            if len(item) == 1:
                dic['label'] = item[0]
                dic['name'] = item[0]
            elif len(item) == 2:
                dic['label'] = item[0]
                dic['name'] = item[1]
            else:
                raise ValueError('Label group takes 1 or 2 arguments')
            group_dicts.append(dic)
    return group_dicts


def parse_arguments(skip=False):
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description='Script to print the list of issues and pull requests '
        'closed in a given milestone, tag including additional filtering '
        'options.')

    # Get common parser arguments
    parser = add_common_parser_args(parser)

    parser.add_argument(
        '-m',
        '--milestone',
        action="store",
        dest="milestone",
        default='',
        help="Github milestone to get issues and pull requests for")
    parser.add_argument(
        '-zr',
        '--zenhub-release',
        action="store",
        dest="zenhub_release",
        default='',
        help="Zenhub release to get issues and pull requests for")
    parser.add_argument(
        '-st',
        '--since-tag',
        action="store",
        dest="since_tag",
        default='',
        help="Github issues and pull requests since tag")
    parser.add_argument(
        '-ut',
        '--until-tag',
        action="store",
        dest="until_tag",
        default='',
        help="Github issues and pull requests until tag")
    parser.add_argument(
        '-b',
        '--branch',
        action="store",
        dest="branch",
        default='',
        help="Github base branch for merged PRs")
    parser.add_argument(
        '-ilg',
        '--issue-label-group',
        action="append",
        nargs='+',
        default=[],
        dest="issue_label_groups",
        help="Groups the generated issues by the specified label. This option"
        "takes 1 or 2 arguments, where the first one is the label to "
        "match and the second one is the label to print on the final"
        "output")
    parser.add_argument(
        '-plg',
        '--pr-label-group',
        action="append",
        nargs='+',
        default=[],
        dest="pr_label_groups",
        help="Groups the generated PRs by the specified label. This option"
        "takes 1 or 2 arguments, where the first one is the label to "
        "match and the second one is the label to print on the final"
        "output")
    parser.add_argument(
        '-lg',
        '--label-group',
        action="append",
        nargs='+',
        default=[],
        dest="label_groups",
        help="Groups the generated issues and PRs by the specified label. "
        "This option takes 1 or 2 arguments, where the first one is the "
        "label to match and the second one is the label to print on "
        "the final output")
    parser.add_argument(
        '-ilr',
        '--issue-label-regex',
        action="store",
        dest="issue_label_regex",
        default='',
        help="Label issue filter using a regular expression filter")
    parser.add_argument(
        '-plr',
        '--pr-label-regex',
        action="store",
        dest="pr_label_regex",
        default='',
        help="Label pull request filter using a regular expression filter")
    parser.add_argument(
        '-f',
        '--format',
        action="store",
        dest="output_format",
        default='changelog',
        help="Format for print, either 'changelog' (for "
        "Changelog.md file) or 'release' (for the Github "
        "Releases page). Default is 'changelog'. The "
        "'release' option doesn't generate Markdown "
        "hyperlinks.")
    parser.add_argument(
        '--template',
        action="store",
        dest="template",
        default='',
        help="Use a custom Jinja2 template file ")
    parser.add_argument(
        '--batch',
        action="store",
        dest="batch",
        default=None,
        choices=['milestones', 'tags'],
        help="Run loghub for all milestones or all tags")
    parser.add_argument(
        '--no-prs',
        action="store_false",
        dest="show_prs",
        default=True,
        help="Run loghub without any pull requests output")
    parser.add_argument(
        '--no-related-prs',
        action="store_false",
        dest="show_related_prs",
        default=True,
        help="Do not display related prs on issues")
    parser.add_argument(
        '--no-related-issues',
        action="store_false",
        dest="show_related_issues",
        default=True,
        help="Do not display related issues on prs")

    options = parser.parse_args()

    milestone = options.milestone
    zenhub_release = options.zenhub_release
    batch = options.batch

    # Check if milestone, release or tag given
    if not batch:
        if not milestone and not zenhub_release and not options.since_tag and not options.until_tag:
            print('\nLOGHUB: Querying all issues\n')
        elif milestone and not zenhub_release and not options.since_tag and not options.until_tag:
            print('\nLOGHUB: Querying issues for milestone "{0}"'
                  '\n'.format(milestone))
        elif zenhub_release and not milestone and not options.since_tag and not options.until_tag:
            print('\nLOGHUB: Querying issues for zenhub release "{0}"'
                  '\n'.format(zenhub_release))
        elif options.since_tag and not options.until_tag and not milestone and not zenhub_release:
            print('\nLOGHUB: Querying issues since tag "{0}"'
                  '\n'.format(options.since_tag))
        elif options.since_tag and options.until_tag and not milestone and not zenhub_release:
            print('\nLOGHUB: Querying issues since tag "{0}" until tag "{1}"'
                  '\n'.format(options.since_tag, options.until_tag))
        else:
            print('Invalid set of options!')
            sys.exit(1)
    elif batch and any([
            bool(options.since_tag), bool(options.until_tag),
            bool(milestone), bool(zenhub_release),
    ]):
        print('LOGHUB: When using batch mode no tags or milestone '
              ' or zenhub release arguments are allowed.\n')
        sys.exit(1)

    # Ask for password once input is valid
    username = options.username
    password = parse_password_check_repo(options)
    try:
        issue_label_groups = options.label_groups + \
                             options.issue_label_groups
        new_issue_label_groups = create_label_groups(issue_label_groups)
    except ValueError:
        print('LOGHUB: Issue label group takes 1 or 2 arguments\n')
        sys.exit(1)

    try:
        pr_label_groups = options.label_groups + options.pr_label_groups
        new_pr_label_groups = create_label_groups(pr_label_groups)
    except ValueError:
        print('LOGHUB: PR label group takes 1 or 2 arguments\n')
        sys.exit(1)

    # Inform users that username and password are deprecated by Github API
    check_github_deprecation(options.username, options.password)

    github_token = options.token
    zenhub_token = options.zenhub_token

    # Check for configuration file in home folder
    config = load_config()
    if config:
        try:
            github_token = config.get('github', 'token')
        except Exception:
            github_token = options.token

        try:
            zenhub_token = config.get('zenhub', 'token')
        except Exception:
            zenhub_token = options.zenhub_token

    if not skip:
        create_changelog(
            repo=options.repository,
            username=username,
            password=password,
            token=github_token,
            milestone=milestone,
            zenhub_release=zenhub_release,
            zenhub_token=zenhub_token,
            since_tag=options.since_tag,
            until_tag=options.until_tag,
            branch=options.branch,
            issue_label_regex=options.issue_label_regex,
            pr_label_regex=options.pr_label_regex,
            output_format=options.output_format,
            template_file=options.template,
            issue_label_groups=new_issue_label_groups,
            pr_label_groups=new_pr_label_groups,
            batch=batch,
            show_prs=options.show_prs,
            show_related_prs=options.show_related_prs,
            show_related_issues=options.show_related_issues,
        )

    return options


if __name__ == '__main__':  # yapf: disable
    main()
