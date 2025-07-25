from __future__ import absolute_import
from __future__ import print_function

import os
import os.path
import json

from .build_yaml import Rule, DocumentationNotComplete
from .constants import (
    MULTI_PLATFORM_LIST, OSCAP_VALUE, datastream_namespace,
    xlink_namespace, XCCDF12_NS, SCE_SYSTEM
)
from .jinja import process_file
from .rules import get_rule_dir_id, get_rule_dir_sces, find_rule_dirs_in_paths
from . import utils, products


def write_sce_file(sce_content, output_dir, filename):
    with open(os.path.join(output_dir, filename), 'w') as output_file:
        print(sce_content, file=output_file)


def load_sce_and_metadata(file_path, local_env_yaml):
    """
    For the given SCE audit file (file_path) under the specified environment
    (local_env_yaml), parse the file while expanding Jinja macros and read any
    metadata headers the file contains. Note that the last keyword of a
    specified type is the recorded one.

    Returns (audit_content, metadata).
    """

    raw_content = process_file(file_path, local_env_yaml)
    return load_sce_and_metadata_parsed(raw_content)


def _process_raw_content_line(line, sce_content, metadata):
    found_metadata = False
    keywords = ['platform', 'check-import', 'check-export', 'complex-check', 'environment']
    for keyword in keywords:
        if not line.startswith('# ' + keyword + ' = '):
            continue
        found_metadata = True
        # Strip off the initial comment marker
        _, value = line[2:].split('=', maxsplit=1)
        metadata[keyword] = value.strip()

    if not found_metadata:
        sce_content.append(line)


def _parse_metadata(raw_content):
    metadata = dict()
    sce_content = []
    shebang = "#!/usr/bin/bash"
    for line in raw_content.split("\n"):
        if line.startswith("#!"):
            shebang = line
            continue
        _process_raw_content_line(line, sce_content, metadata)
    return shebang, "\n".join(sce_content), metadata


def _set_metadata_default_values(metadata):
    if 'check-export' in metadata:
        # Special case for the variables exposed to the SCE script: prepend
        # the OSCAP_VALUE prefix to reference the variable
        new_variables = []
        for value in metadata['check-export'].split(','):
            k, v = value.split('=', maxsplit=1)
            new_variables.append(k+'='+OSCAP_VALUE+v)
        metadata['check-export'] = new_variables

    if 'platform' in metadata:
        metadata['platform'] = metadata['platform'].split(',')
    else:
        metadata['platform'] = ['multi_platform_all']

    if "environment" not in metadata:
        metadata["environment"] = "any"
    environment_options = ["normal", "bootc", "any"]
    if metadata["environment"] not in environment_options:
        raise RuntimeError(
            "Wrong value of the 'environment' headers: '%s'. It needs to be "
            "one of %s" % (
                metadata["environment"], ", ".join(environment_options))
        )


def _modify_sce_with_environment(sce_content, environment):
    if environment == "any":
        return sce_content
    if environment == "bootc":
        condition = "(rpm -q --quiet bootc && [ -e /run/.containerenv ])"
    if environment == "normal":
        condition = "! (rpm -q --quiet bootc && [ -e /run/.containerenv ])"
    lines = list(sce_content.split("\n"))
    for i in range(len(lines)):
        if len(lines[i]) > 0:
            lines[i] = (4 * " ") + lines[i]
    lines.insert(0, "if " + condition + " ; then")
    lines.append("else")
    lines.append("    echo \"The SCE check can't run in this environment.\"")
    lines.append("    exit \"$XCCDF_RESULT_ERROR\"")
    lines.append("fi")
    return "\n".join(lines)


def load_sce_and_metadata_parsed(raw_content):
    shebang, sce_content, metadata = _parse_metadata(raw_content)
    _set_metadata_default_values(metadata)
    sce_content = _modify_sce_with_environment(sce_content, metadata["environment"])
    sce_content = shebang + "\n" + sce_content
    return sce_content, metadata


def _check_is_loaded(already_loaded, filename):
    # Right now this check doesn't look at metadata or anything
    # else. Eventually we might add versions to the entry or
    # something.
    return filename in already_loaded


# Retrieve the SCE checks and return a list of path to each check script.
def collect_sce_checks(datastreamtree):
    checklists = datastreamtree.find(
        ".//{%s}checklists" % datastream_namespace)
    checklists_component_ref = checklists.find(
        "{%s}component-ref" % datastream_namespace)
    # The component ID is the component-ref href without leading '#'
    checklist_component_id = checklists_component_ref.get('{%s}href' % xlink_namespace)[1:]

    checks_xpath = str.format(
        ".//{{{ds_ns}}}component[@id='{cid}']/"
        "{{{xccdf_ns}}}Benchmark//"
        "{{{xccdf_ns}}}Rule//"
        "{{{xccdf_ns}}}check[@system='{sce_sys}']/"
        "{{{xccdf_ns}}}check-content-ref",
        ds_ns=datastream_namespace,
        xccdf_ns=XCCDF12_NS,
        cid=checklist_component_id,
        sce_sys=SCE_SYSTEM
    )

    checks = datastreamtree.findall(checks_xpath)
    # Extract the file paths of the SCE checks
    return [check.get('href') for check in checks]


class SCEBuilder():
    def __init__(self, env_yaml, product_yaml, template_builder, output_dir):
        self.env_yaml = env_yaml
        self.product_yaml = product_yaml
        self.template_builder = template_builder
        self.output_dir = output_dir
        self.already_loaded = dict()

    def _build_static_sce_check(self, rule_id, path, local_env_yaml):
        # To be compatible with later checks, use the rule_id (i.e., the
        # value of _dir) to recreate the expected filename if this OVAL
        # was in a rule directory. However, note that unlike
        # build_oval.checks(...), we have to get this script's extension
        # first.
        _, ext = os.path.splitext(path)
        filename = "{0}{1}".format(rule_id, ext)

        sce_content, metadata = load_sce_and_metadata(path, local_env_yaml)
        metadata['filename'] = filename
        product = utils.required_key(self.env_yaml, "product")

        if not utils.is_applicable_for_product(",".join(metadata["platform"]), product):
            return
        if _check_is_loaded(self.already_loaded, rule_id):
            return

        write_sce_file(sce_content, self.output_dir, filename)

        self.already_loaded[rule_id] = metadata

    def _get_rule_sce_lang(self, rule):
        langs = self.template_builder.get_resolved_langs_to_generate(rule)
        for lang in langs:
            if lang.name == 'sce-bash':
                return lang
        return None

    def _build_templated_sce_check(self, rule):
        if not rule.template:
            return
        sce_lang = self._get_rule_sce_lang(rule)
        if sce_lang is None:
            return

        # Here we know the specified rule has a template and this
        # template actually generates (bash) SCE content. We
        # prioritize bespoke SCE content over templated content,
        # however, while we add this to our metadata, we do not
        # bother (yet!) with generating the SCE content. This is done
        # at a later time by build-scripts/build_templated_content.py.
        if _check_is_loaded(self.already_loaded, rule.id_):
            return

        # While we don't _write_ it, we still need to parse SCE
        # metadata from the templated content. Render it internally.
        raw_sce_content = self.template_builder.get_lang_contents_for_templatable(
            rule, sce_lang
        )

        ext = '.sh'
        filename = rule.id_ + ext

        # Load metadata and infer correct file name.
        sce_content, metadata = load_sce_and_metadata_parsed(raw_sce_content)
        metadata['filename'] = filename

        # Skip the check if it isn't applicable for this product.
        product = utils.required_key(self.env_yaml, "product")
        if not utils.is_applicable_for_product(",".join(metadata["platform"]), product):
            return

        write_sce_file(sce_content, self.output_dir, filename)

        # Finally, include it in our loaded content
        self.already_loaded[rule.id_] = metadata

    def _build_rule(self, rule_dir_path):
        local_env_yaml = dict()
        local_env_yaml.update(self.env_yaml)
        product = utils.required_key(self.env_yaml, "product")
        rule_id = get_rule_dir_id(rule_dir_path)

        rule_path = os.path.join(rule_dir_path, "rule.yml")
        try:
            rule = Rule.from_yaml(rule_path, self.env_yaml)
        except DocumentationNotComplete:
            # Happens on non-debug builds when a rule isn't yet completed. We
            # don't want to build the SCE check for this rule yet so skip it
            # and move on.
            return

        local_env_yaml['rule_id'] = rule.id_
        local_env_yaml['rule_title'] = rule.title
        local_env_yaml['products'] = {product}

        for _path in get_rule_dir_sces(rule_dir_path, product):
            self._build_static_sce_check(rule_id, _path, local_env_yaml)

        self._build_templated_sce_check(rule)

    def _dump_metadata(self):
        # Finally, write out our metadata to disk so that we can reference it in
        # later build stages (such as during building shorthand content).
        metadata_path = os.path.join(self.output_dir, 'metadata.json')
        json.dump(self.already_loaded, open(metadata_path, 'w'))

    def _find_content_dirs(self):
        # We maintain the same search structure as build_ovals.py even though we
        # don't currently have any content under shared/checks/sce.
        product_dir = self.product_yaml["product_dir"]
        relative_guide_dir = utils.required_key(self.env_yaml, "benchmark_root")
        guide_dir = os.path.abspath(os.path.join(product_dir, relative_guide_dir))
        additional_content_directories = self.env_yaml.get(
            "additional_content_directories", [])
        add_content_dirs = [
            os.path.abspath(os.path.join(product_dir, rd))
            for rd in additional_content_directories
        ]
        return ([guide_dir] + add_content_dirs)

    def build(self):
        """
        Walks the content repository and builds all SCE checks (and metadata entry)
        into the output directory.
        """
        content_dirs = self._find_content_dirs()
        for _dir_path in find_rule_dirs_in_paths(content_dirs):
            self._build_rule(_dir_path)
        self._dump_metadata()
