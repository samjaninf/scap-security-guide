"""
Common functions for processing Ansible in SSG
"""

from __future__ import absolute_import
from __future__ import print_function

import re

from .constants import ansible_version_requirement_pre_task_name
from .constants import min_ansible_version
from .constants import REF_PREFIX_MAP


def add_minimum_version(ansible_src):
    """
    Adds minimum ansible version to an Ansible script
    """
    pre_task = (""" - hosts: all
   pre_tasks:
     - name: %s
       assert:
         that: "ansible_version.full is version_compare('%s', '>=')"
         msg: >
           "You must update Ansible to at least version %s to use this role."
          """ % (ansible_version_requirement_pre_task_name,
                 min_ansible_version, min_ansible_version))

    if ' - hosts: all' not in ansible_src:
        return ansible_src

    if 'pre_task' in ansible_src:
        if 'ansible_version.full is version_compare' in ansible_src:
            return ansible_src

        raise ValueError(
            "A pre_task already exists in ansible_src; failing to process: %s" %
            ansible_src)

    return ansible_src.replace(" - hosts: all", pre_task, 1)


def add_play_name(ansible_src, profile):
    old_play_start = r"^( *)- hosts: all"
    new_play_start = (
        r"\1- name: Ansible Playbook for %s\n\1  hosts: all" % (profile))
    return re.sub(old_play_start, new_play_start, ansible_src, flags=re.M)


def remove_too_many_blank_lines(ansible_src):
    """
    Condenses three or more empty lines as two.
    """
    return re.sub(r'\n{4,}', '\n\n\n', ansible_src, 0, flags=re.M)


def remove_trailing_whitespace(ansible_src):
    """
    Removes trailing whitespace in an Ansible script
    """
    return re.sub(r'[ \t]+$', '', ansible_src, 0, flags=re.M)


def strip_eof(ansible_src):
    """
    Removes extra newlines at end of file
    """
    return ansible_src.rstrip() + "\n"


def _strings_to_list(one_or_more_strings):
    """
    Output a list, that either contains one string, or a list of strings.
    In Python, strings can be cast to lists without error, but with unexpected result.
    """
    if isinstance(one_or_more_strings, str):
        return [one_or_more_strings]
    else:
        return list(one_or_more_strings)


def update_yaml_list_or_string(current_contents, new_contents):
    result = []
    if current_contents:
        result += _strings_to_list(current_contents)
    if new_contents:
        result += _strings_to_list(new_contents)
    if not result:
        result = ""
    if len(result) == 1:
        result = result[0]
    return result
