# platform = multi_platform_all
# reboot = true
# strategy = restrict
# complexity = low
# disruption = low

{{{ bash_selinux_config_set(parameter="SELINUX", value="permissive", rule_id=rule_id) }}}

fixfiles onboot
