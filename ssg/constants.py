from __future__ import absolute_import
from __future__ import print_function

import os.path
import os
import time
import collections


SSG_PROJECT_NAME = "SCAP Security Guide Project"
SSG_BENCHMARK_LATEST_URI = "https://github.com/ComplianceAsCode/content/releases/latest"

SSG_REF_URIS = {
    'anssi': 'https://cyber.gouv.fr/sites/default/files/document/linux_configuration-en-v2.pdf',
    'bsi': 'https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Grundschutz/International/bsi_it_gs_comp_2022.pdf',
    'nist': 'http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r4.pdf',
    'nist-csf': 'https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04162018.pdf',
    'isa-62443-2013': 'https://www.isa.org/products/ansi-isa-62443-3-3-99-03-03-2013-security-for-indu',
    'isa-62443-2009': 'https://www.isa.org/products/isa-62443-2-1-2009-security-for-industrial-automat',
    'cobit5': 'https://www.isaca.org/resources/cobit',
    'cis-csc': 'https://www.cisecurity.org/controls/',
    'cjis': 'https://www.fbi.gov/file-repository/cjis-security-policy-v5_5_20160601-2-1.pdf',
    'cui': 'http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171.pdf',
    'dcid': 'not_officially_available',
    'disa': 'https://public.cyber.mil/stigs/cci/',
    'pcidss': 'https://www.pcisecuritystandards.org/documents/PCI_DSS_v3-2-1.pdf',
    'pcidss4': 'https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0.pdf',
    'ospp': 'https://www.niap-ccevs.org/Profile/PP.cfm',
    'hipaa': 'https://www.gpo.gov/fdsys/pkg/CFR-2007-title45-vol1/pdf/CFR-2007-title45-vol1-chapA-subchapC.pdf',
    'ism': 'https://www.cyber.gov.au/acsc/view-all-content/ism',
    'iso27001-2013': 'https://www.iso.org/contents/data/standard/05/45/54534.html',
    'nerc-cip': 'https://www.nerc.com/pa/Stand/AlignRep/One%20Stop%20Shop.xlsx',
    'stigid': 'https://public.cyber.mil/stigs/downloads/?_dl_facet_stigs=operating-systems%2Cunix-linux',
    'os-srg': 'https://public.cyber.mil/stigs/downloads/?_dl_facet_stigs=operating-systems%2Cgeneral-purpose-os',
    'app-srg': 'https://public.cyber.mil/stigs/downloads/?_dl_facet_stigs=application-servers',
    'app-srg-ctr': 'https://public.cyber.mil/stigs/downloads/?_dl_facet_stigs=container-platform',
    'stigref': 'https://public.cyber.mil/stigs/srg-stig-tools/',
}

product_directories = [
    'alinux2',
    'alinux3',
    'almalinux9',
    'anolis8',
    'anolis23',
    'al2023',
    'chromium',
    'debian11', 'debian12', 'debian13',
    'example',
    'eks',
    'fedora',
    'firefox',
    'kylinserver10',
    'ocp4',
    'rhcos4',
    'ol7', 'ol8', 'ol9', 'ol10',
    'openeuler2203',
    'opensuse',
    'openembedded',
    'rhel8', 'rhel9', 'rhel10',
    'rhv4',
    'sle12', 'sle15', 'slmicro5', 'slmicro6',
    'tencentos4',
    'ubuntu2204', 'ubuntu2404'
]

JINJA_MACROS_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(
    __file__)), "shared", "macros"))

xml_version = """<?xml version="1.0" encoding="UTF-8"?>"""

datastream_namespace = "http://scap.nist.gov/schema/scap/source/1.2"
dc_namespace = "http://purl.org/dc/elements/1.1/"
ocil_namespace = "http://scap.nist.gov/schema/ocil/2.0"
cpe_language_namespace = "http://cpe.mitre.org/language/2.0"
cpe_dictionary_namespace = "http://cpe.mitre.org/dictionary/2.0"
oval_footer = "</oval_definitions>"
oval_namespace = "http://oval.mitre.org/XMLSchema/oval-definitions-5"
xlink_namespace = "http://www.w3.org/1999/xlink"
xhtml_namespace = "http://www.w3.org/1999/xhtml"
xsi_namespace = "http://www.w3.org/2001/XMLSchema-instance"
cat_namespace = "urn:oasis:names:tc:entity:xmlns:xml:catalog"
sce_namespace = "http://open-scap.org/page/SCE_xccdf_stream"
ocil_cs = "http://scap.nist.gov/schema/ocil/2"
bash_system = "urn:xccdf:fix:script:sh"
ansible_system = "urn:xccdf:fix:script:ansible"
ignition_system = "urn:xccdf:fix:script:ignition"
kubernetes_system = "urn:xccdf:fix:script:kubernetes"
blueprint_system = "urn:redhat:osbuild:blueprint"
puppet_system = "urn:xccdf:fix:script:puppet"
anaconda_system = "urn:redhat:anaconda:pre"
kickstart_system = "urn:xccdf:fix:script:kickstart"
bootc_system = "urn:xccdf:fix:script:bootc"
cce_uri = "https://ncp.nist.gov/cce"
stig_ns = "https://public.cyber.mil/stigs/srg-stig-tools/"
ccn_ns = "https://www.ccn-cert.cni.es/pdf/guias/series-ccn-stic/guias-de-acceso-publico-ccn-stic/6768-ccn-stic-610a22-perfilado-de-seguridad-red-hat-enterprise-linux-9-0/file.html"
cis_ns = "https://www.cisecurity.org/benchmark/red_hat_linux/"
hipaa_ns = "https://www.gpo.gov/fdsys/pkg/CFR-2007-title45-vol1/pdf/CFR-2007-title45-vol1-chapA-subchapC.pdf"
anssi_ns = "https://cyber.gouv.fr/sites/default/files/document/linux_configuration-en-v2.pdf"
ospp_ns = "https://www.niap-ccevs.org/Profile/PP.cfm"
pcidss4_ns = "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0.pdf"
cui_ns = 'http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171.pdf'
stig_refs = 'https://public.cyber.mil/stigs/'
disa_cciuri = "https://public.cyber.mil/stigs/cci/"
ssg_version_uri = \
    "https://github.com/ComplianceAsCode/content/releases/latest"
OSCAP_VENDOR = "org.ssgproject"
OSCAP_DS_STRING = "xccdf_%s.content_benchmark_" % OSCAP_VENDOR
OSCAP_BENCHMARK = "xccdf_%s.content_benchmark_" % OSCAP_VENDOR
OSCAP_PROFILE = "xccdf_%s.content_profile_" % OSCAP_VENDOR
OSCAP_GROUP = "xccdf_%s.content_group_" % OSCAP_VENDOR
OSCAP_RULE = "xccdf_%s.content_rule_" % OSCAP_VENDOR
OSCAP_VALUE = "xccdf_%s.content_value_" % OSCAP_VENDOR
OSCAP_GROUP_PCIDSS = "xccdf_%s.content_group_pcidss-req" % OSCAP_VENDOR
OSCAP_GROUP_VAL = "xccdf_%s.content_group_values" % OSCAP_VENDOR
OSCAP_GROUP_NON_PCI = "xccdf_%s.content_group_non-pci-dss" % OSCAP_VENDOR
OSCAP_PATH = "oscap"
OSCAP_PROFILE_ALL_ID = "(all)"
XCCDF11_NS = "http://checklists.nist.gov/xccdf/1.1"
XCCDF12_NS = "http://checklists.nist.gov/xccdf/1.2"
min_ansible_version = "2.9"
ansible_version_requirement_pre_task_name = \
    "Verify Ansible meets SCAP-Security-Guide version requirements."
standard_profiles = ['standard', 'pci-dss', 'desktop', 'server']
xslt_ns = "http://www.w3.org/1999/XSL/Transform"
SCE_SYSTEM = "http://open-scap.org/page/SCE"


OVAL_SUB_NS = dict(
    ind="independent",
    unix="unix",
    linux="linux",
)


PREFIX_TO_NS = {
    "oval-def": oval_namespace,
    "oval": "http://oval.mitre.org/XMLSchema/oval-common-5",
    "dc": dc_namespace,
    "ds": datastream_namespace,
    "ocil": ocil_namespace,
    "xccdf-1.1": XCCDF11_NS,
    "xccdf-1.2": XCCDF12_NS,
    "html": xhtml_namespace,
    "xlink": xlink_namespace,
    "cpe-dict": cpe_dictionary_namespace,
    "cat": cat_namespace,
    "cpe-lang": cpe_language_namespace,
    "sce": sce_namespace,
}

FIX_TYPE_TO_SYSTEM = {
    "bash": bash_system,
    "ansible": ansible_system,
    "ignition": ignition_system,
    "kubernetes": kubernetes_system,
    "blueprint": blueprint_system,
    "puppet": puppet_system,
    "anaconda": anaconda_system,
    "kickstart": kickstart_system,
    "bootc": bootc_system,
}

for prefix, url_part in OVAL_SUB_NS.items():
    assert prefix not in PREFIX_TO_NS, \
        "Conflict between a namespace and OVAL sub-namespace '{prefix}'".format(prefix=prefix)
    PREFIX_TO_NS[prefix] = "{oval_ns}#{suffix}".format(oval_ns=PREFIX_TO_NS["oval-def"], suffix=url_part)


oval_header = (
    """
<oval_definitions
    xmlns="{0}"
    xmlns:oval="http://oval.mitre.org/XMLSchema/oval-common-5"
    xmlns:ind="{0}#independent"
    xmlns:unix="{0}#unix"
    xmlns:linux="{0}#linux"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://oval.mitre.org/XMLSchema/oval-common-5 oval-common-schema.xsd
        {0} oval-definitions-schema.xsd
        {0}#independent independent-definitions-schema.xsd
        {0}#unix unix-definitions-schema.xsd
        {0}#linux linux-definitions-schema.xsd">"""
    .format(oval_namespace))

_timestamp = time.gmtime(int(os.environ.get('SOURCE_DATE_EPOCH', time.time())))

timestamp = time.strftime(
    "%Y-%m-%dT%H:%M:%S",
    _timestamp
)

timestamp_yyyy_mm_dd = time.strftime(
    "%Y-%m-%d",
    _timestamp
)

PKG_MANAGER_TO_SYSTEM = {
    "yum": "rpm",
    "zypper": "rpm",
    "dnf": "rpm",
    "apt_get": "dpkg",
}

PKG_MANAGER_TO_CONFIG_FILE = {
    "yum": "/etc/yum.conf",
    "dnf": "/etc/dnf/dnf.conf",
    "zypper": "/etc/zypp/zypper.conf",
}

FULL_NAME_TO_PRODUCT_MAPPING = {
    "Alibaba Cloud Linux 2": "alinux2",
    "Alibaba Cloud Linux 3": "alinux3",
    "AlmaLinux OS 9": "almalinux9",
    "Anolis OS 8": "anolis8",
    "Anolis OS 23": "anolis23",
    "Amazon Linux 2023": "al2023",
    "Chromium": "chromium",
    "Debian 11": "debian11",
    "Debian 12": "debian12",
    "Debian 13": "debian13",
    "Example": "example",
    "Amazon Elastic Kubernetes Service": "eks",
    "Fedora": "fedora",
    "Firefox": "firefox",
    "Kylin Server 10": "kylinserver10",
    "Red Hat OpenShift Container Platform 4": "ocp4",
    "Red Hat Enterprise Linux CoreOS 4": "rhcos4",
    "Oracle Linux 7": "ol7",
    "Oracle Linux 8": "ol8",
    "Oracle Linux 9": "ol9",
    "Oracle Linux 10": "ol10",
    "openEuler 2203": "openeuler2203",
    "openSUSE": "opensuse",
    "Red Hat Enterprise Linux 8": "rhel8",
    "Red Hat Enterprise Linux 9": "rhel9",
    "Red Hat Enterprise Linux 10": "rhel10",
    "Red Hat Virtualization 4": "rhv4",
    "SUSE Linux Enterprise 12": "sle12",
    "SUSE Linux Enterprise 15": "sle15",
    "SUSE Linux Enterprise Micro 5": "slmicro5",
    "SUSE Linux Enterprise Micro 6": "slmicro6",
    "TencentOS Server 4": "tencentos4",
    "Ubuntu 22.04": "ubuntu2204",
    "Ubuntu 24.04": "ubuntu2404",
    "OpenEmbedded": "openembedded",
    "Not Applicable": "example",
}


# see xccdf-addremediations.xslt <- shared_constants.xslt
# if you want to know how the map was constructed
REF_PREFIX_MAP = {
    "nist": "NIST-800-53",
    "cui": "NIST-800-171",
    "pcidss": "PCI-DSS",
    "pcidss4": "PCI-DSSv4",
    "cjis": "CJIS",
    "stigid": "DISA-STIG",
}

Reference = collections.namedtuple("Reference", ("id", "name", "url", "regex_with_groups"))

REFERENCES = dict(
    anssi=Reference(
        id="anssi", name="ANSSI", url=anssi_ns,
        regex_with_groups=r"R(\d+)"),
    ccn=Reference(
        id="ccn", name="CCN", url="",
        regex_with_groups=r"A\.(\d+)\.SEC-(\w+)(\d+)"),
    cis=Reference(
        id="cis", name="CIS", url=cis_ns,
        regex_with_groups=r"(\d+)\.(\d+)(?:\.(\w+)(?:\.(\w+)(?:\.(\w+))?)?)?"),
    cui=Reference(
        id="cui", name=REF_PREFIX_MAP["cui"], url=cui_ns,
        regex_with_groups=r"(\d+)(?:\.(\w+)(?:\.(\w+)(?:\.(\w+))?)?)?"),
    nist=Reference(
        id="nist", name=REF_PREFIX_MAP["nist"], url="",
        regex_with_groups=r".*-(\d+)(?:\((\d+)\))?"),
    ospp=Reference(
        id="ospp", name="OSPP", url=SSG_REF_URIS["ospp"],
        regex_with_groups=r"(\w+)(?:\.(\d+)(?:\.([^\.]+)(?:\.([^\.]+))?)?)?"),
    pcidss=Reference(
        id="pcidss", name=REF_PREFIX_MAP["pcidss"], url="",
        regex_with_groups=r"Req-(\d+)(?:\.(\w+)(?:\.(\w+)(?:\.(\w+))?)?)?"),
    pcidss4=Reference(
        id="pcidss4", name=REF_PREFIX_MAP["pcidss4"], url="",
        regex_with_groups=r"(\d+)(?:\.(\w+)(?:\.(\w+)(?:\.(\w+))?)?)?"),
    srg=Reference(
        id="srg", name="SRG", url="",
        regex_with_groups=r"(SRG-OS-\d+-GPOS-\d+)"
    )
)


MULTI_PLATFORM_LIST = ["rhel", "fedora", "rhv", "debian", "ubuntu",
                       "openeuler", "kylinserver",
                       "opensuse", "sle", "tencentos", "ol", "ocp", "rhcos",
                       "example", "eks", "alinux", "anolis", "openembedded", "al",
                       "slmicro", "almalinux"]

MULTI_PLATFORM_MAPPING = {
    "multi_platform_alinux": ["alinux2", "alinux3"],
    "multi_platform_almalinux": ["almalinux9"],
    "multi_platform_anolis": ["anolis8", "anolis23"],
    "multi_platform_debian": ["debian11", "debian12", "debian13"],
    "multi_platform_example": ["example"],
    "multi_platform_eks": ["eks"],
    "multi_platform_fedora": ["fedora"],
    "multi_platform_kylinserver": ["kylinserver10"],
    "multi_platform_openeuler": ["openeuler2203"],
    "multi_platform_opensuse": ["opensuse"],
    "multi_platform_ol": ["ol7", "ol8", "ol9", "ol10"],
    "multi_platform_ocp": ["ocp4"],
    "multi_platform_rhcos": ["rhcos4"],
    "multi_platform_rhel": ["rhel8", "rhel9", "rhel10"],
    "multi_platform_rhv": ["rhv4"],
    "multi_platform_sle": ["sle12", "sle15"],
    "multi_platform_slmicro": ["slmicro5", "slmicro6"],
    "multi_platform_tencentos": ["tencentos4"],
    "multi_platform_ubuntu": ["ubuntu2204", "ubuntu2404"],
    "multi_platform_openembedded": ["openembedded"],
    "multi_platform_al": ["al2023"],
}

RHEL_CENTOS_CPE_MAPPING = {
    "cpe:/o:redhat:enterprise_linux:8": "cpe:/o:centos:centos:8",
    "cpe:/o:redhat:enterprise_linux:9": "cpe:/o:centos:centos:9",
    "cpe:/o:redhat:enterprise_linux:10": "cpe:/o:centos:centos:10",
}

CENTOS_NOTICE = \
    "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n" \
    "<p>This benchmark is a direct port of a <i>SCAP Security Guide </i> " \
    "benchmark developed for <i>Red Hat Enterprise Linux</i>. It has been " \
    "modified through an automated process to remove specific dependencies " \
    "on <i>Red Hat Enterprise Linux</i> and to function with <i>CentOS</i>. " \
    "The result is a generally useful <i>SCAP Security Guide</i> benchmark " \
    "with the following caveats:</p>\n" \
    "<ul>\n" \
    "<li><i>CentOS</i> is not an exact copy of " \
    "<i>Red Hat Enterprise Linux</i>. There may be configuration differences " \
    "that produce false positives and/or false negatives. If this occurs " \
    "please file a bug report.</li>\n" \
    "\n" \
    "<li><i>CentOS</i> has its own build system, compiler options, patchsets, " \
    "and is a community supported, non-commercial operating system. " \
    "<i>CentOS</i> does not inherit " \
    "certifications or evaluations from <i>Red Hat Enterprise Linux</i>. As " \
    "such, some configuration rules (such as those requiring " \
    "<i>FIPS 140-2</i> encryption) will continue to fail on <i>CentOS</i>.</li>\n" \
    "</ul>\n" \
    "\n" \
    "<p>Members of the <i>CentOS</i> community are invited to participate in " \
    "<a href=\"http://open-scap.org\">OpenSCAP</a> and " \
    "<a href=\"https://github.com/ComplianceAsCode/content\">" \
    "SCAP Security Guide</a> development. Bug reports and patches " \
    "can be sent to GitHub: " \
    "<a href=\"https://github.com/ComplianceAsCode/content\">" \
    "https://github.com/ComplianceAsCode/content</a>. " \
    "The mailing list is at " \
    "<a href=\"https://fedorahosted.org/mailman/listinfo/scap-security-guide\">" \
    "https://fedorahosted.org/mailman/listinfo/scap-security-guide</a>" \
    ".</p>" \
    "</div>"

XCCDF_REFINABLE_PROPERTIES = ["weight", "severity", "role", "selector"]

OVAL_TO_XCCDF_DATATYPE_CONSTRAINTS = {
    'int': 'number',
    'float': 'number',
    'boolean': 'boolean',
    'string': 'string',
    'evr_string': 'string',
    'version': 'string',
    'ios_version': 'string',
    'fileset_revision': 'string',
    'binary': 'string'
}

OVALTAG_TO_ABBREV = {
    'definition': 'def',
    'criteria': 'crit',
    'test': 'tst',
    'object': 'obj',
    'state': 'ste',
    'variable': 'var',
}

OCILTAG_TO_ABBREV = {
    'questionnaire': 'questionnaire',
    'action': 'testaction',
    'question': 'question',
    'artifact': 'artifact',
    'variable': 'variable',
}

OVALREFATTR_TO_TAG = {
    "definition_ref": "definition",
    "test_ref": "test",
    "object_ref": "object",
    "state_ref": "state",
    "var_ref": "variable",
}

OCILREFATTR_TO_TAG = {
    "question_ref": "question",
}

# Default platform to package mapping
XCCDF_PLATFORM_TO_PACKAGE = {
  "grub2": "grub2-common",
  "login_defs": "login",
  "sssd": "sssd-common",
  "zipl": "s390utils-base",
  "sssd-ldap": None,  # Force package check wrapping skip
  "uefi": None,
  "non-uefi": None,
  "not_s390x_arch": None,
  "s390x_arch": None,
  "not_aarch64_arch": None,
  "aarch64_arch": None,
  "ovirt": None,
  "no_ovirt": None,
}

# _version_name_map = {
MAKEFILE_ID_TO_PRODUCT_MAP = {
    'alinux': 'Alibaba Cloud Linux',
    'almalinux': 'AlmaLinux OS',
    'anolis': 'Anolis OS',
    'chromium': 'Google Chromium Browser',
    'fedora': 'Fedora',
    'firefox': 'Mozilla Firefox',
    'kylinserver': 'Kylin Server',
    'rhel': 'Red Hat Enterprise Linux',
    'rhv': 'Red Hat Virtualization',
    'debian': 'Debian',
    'ubuntu': 'Ubuntu',
    'eap': 'JBoss Enterprise Application Platform',
    'fuse': 'JBoss Fuse',
    'openeuler': 'openEuler',
    'opensuse': 'openSUSE',
    'sle': 'SUSE Linux Enterprise',
    'slmicro': 'SUSE Linux Enterprise Micro',
    'tencentos': 'TencentOS Server',
    'example': 'Example',
    'ol': 'Oracle Linux',
    'ocp': 'Red Hat OpenShift Container Platform',
    'rhcos': 'Red Hat Enterprise Linux CoreOS',
    'eks': 'Amazon Elastic Kubernetes Service',
    'al': 'Amazon Linux',
    'openembedded': 'OpenEmbedded',
}

# References that can not be used with product-qualifiers
GLOBAL_REFERENCES = ("srg", "disa", "cis-csc",)

# Application constants
DEFAULT_DCONF_GDM_DIR = 'gdm.d'
DEFAULT_AIDE_CONF_PATH = '/etc/aide.conf'
DEFAULT_AIDE_BIN_PATH = '/usr/sbin/aide'
DEFAULT_AUDIT_WATCHES_STYLE = 'legacy'
DEFAULT_RSYSLOG_CAFILE = '/etc/pki/tls/cert.pem'
DEFAULT_FAILLOCK_PATH = '/var/run/faillock'
DEFAULT_SSH_DISTRIBUTED_CONFIG = 'false'
DEFAULT_PRODUCT = 'example'
DEFAULT_CHRONY_CONF_PATH = '/etc/chrony.conf'
DEFAULT_CHRONY_D_PATH = '/etc/chrony.d/'
DEFAULT_AUDISP_CONF_PATH = '/etc/audit'
DEFAULT_SYSCTL_REMEDIATE_DROP_IN_FILE = 'false'
DEFAULT_BOOTABLE_CONTAINERS_SUPPORTED = 'false'
DEFAULT_XWINDOWS_PACKAGES = [ 'xorg-x11-server-Xorg',
                              'xorg-x11-server-common',
                              'xorg-x11-server-utils',
                              'xorg-x11-server-Xwayland']

# Constants for OVAL object model
STR_TO_BOOL = {
    "false": False,
    "False": False,
    "true": True,
    "True": True,
}

BOOL_TO_STR = {True: "true", False: "false"}


class OvalNamespaces:
    oval = "http://oval.mitre.org/XMLSchema/oval-common-5"
    definition = oval_namespace
    independent = "http://oval.mitre.org/XMLSchema/oval-definitions-5#independent"
    linux = "http://oval.mitre.org/XMLSchema/oval-definitions-5#linux"


OVAL_NAMESPACES = OvalNamespaces()

DERIVATIVES_PRODUCT_MAPPING = {
    "centos8": "rhel8",
    "cs9": "rhel9",
    "cs10": "rhel10",
}

BENCHMARKS = {
    "apple_os",
    "applications",
    "linux_os/guide",
    "products/chromium/guide",
    "products/firefox/guide",
}


SSG_IDENT_URIS = {
    'cce': cce_uri
}
