#!/bin/bash
# packages = audit

{{% if "ol" in product or 'rhel' in product %}}
echo "-a always,exit -F arch=b32 -S finit_module -F auid>={{{ uid_min }}} -F auid!=unset -k modules" >> /etc/audit/rules.d/modules.rules
echo "-a always,exit -F arch=b64 -S finit_module -F auid>={{{ uid_min }}} -F auid!=unset -k modules" >> /etc/audit/rules.d/modules.rules
{{% else %}}
echo "-a always,exit -F arch=b32 -S finit_module -k modules" >> /etc/audit/rules.d/modules.rules
echo "-a always,exit -F arch=b64 -S finit_module -k modules" >> /etc/audit/rules.d/modules.rules
{{% endif %}}
