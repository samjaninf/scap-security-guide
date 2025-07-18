---
documentation_complete: true

metadata:
    SMEs:
        - marcusburghardt
        - yuumasato

title: 'ANSSI-BP-028 (high)'

description: |-
    This profile contains configurations that align to ANSSI-BP-028 v2.0 at the high hardening level.

    ANSSI is the French National Information Security Agency, and stands for Agence nationale de la sécurité des systèmes d'information.
    ANSSI-BP-028 is a configuration recommendation for GNU/Linux systems.

    A copy of the ANSSI-BP-028 can be found at the ANSSI website:
    https://www.ssi.gouv.fr/administration/guide/recommandations-de-securite-relatives-a-un-systeme-gnulinux/

    An English version of the ANSSI-BP-028 can also be found at the ANSSI website:
    https://cyber.gouv.fr/publications/configuration-recommendations-gnulinux-system

selections:
    - anssi:all:high
    - var_password_hashing_algorithm=SHA512
    - var_password_pam_unix_rounds=65536
    - var_mount_option_proc_hidepid=invisible
    # the following rule renders UEFI systems unbootable
    - '!sebool_secure_mode_insmod'
    # Following rules once had a prodtype incompatible with the rhel9 product
    - '!partition_for_opt'
    - '!accounts_passwords_pam_tally2_deny_root'
    - '!install_PAE_kernel_on_x86-32'
    - '!partition_for_boot'
    - '!aide_periodic_checking_systemd_timer'
    - '!sudo_add_ignore_dot'
    - '!audit_rules_privileged_commands_rmmod'
    - '!audit_rules_privileged_commands_modprobe'
    - '!package_dracut-fips-aesni_installed'
    - '!cracklib_accounts_password_pam_lcredit'
    - '!partition_for_usr'
    - '!cracklib_accounts_password_pam_ocredit'
    - '!enable_pam_namespace'
    - '!audit_rules_privileged_commands_insmod'
    - '!service_chronyd_or_ntpd_enabled'
    - '!chronyd_configure_pool_and_server'
    - '!accounts_passwords_pam_tally2'
    - '!cracklib_accounts_password_pam_ucredit'
    - '!accounts_passwords_pam_tally2_unlock_time'
    - '!sudo_add_umask'
    - '!sudo_add_env_reset'
    - '!cracklib_accounts_password_pam_minlen'
    - '!cracklib_accounts_password_pam_dcredit'
    - '!ensure_oracle_gpgkey_installed'
    - '!ensure_almalinux_gpgkey_installed'
    - '!package_kea_removed'
    - '!audit_rules_file_deletion_events_renameat2'
    - '!audit_rules_dac_modification_fchmodat2'
    # disable R45: Enable AppArmor security profiles
    - '!apparmor_configured'
    - '!all_apparmor_profiles_enforced'
    - '!grub2_enable_apparmor'
    - '!package_apparmor_installed'
    - '!package_pam_apparmor_installed'
    - '!package_rsh-server_removed'
    - '!package_rsh_removed'
    - '!package_xinetd_removed'
    - '!package_ypbind_removed'
    - '!package_ypserv_removed'

    # RHEL9 unified the paths for grub2 files. These rules are selected in control file by R5 and R29.
    - '!file_groupowner_efi_grub2_cfg'
    - '!file_owner_efi_grub2_cfg'
    - '!file_permissions_efi_grub2_cfg'
    - '!file_groupowner_efi_user_cfg'
    - '!file_owner_efi_user_cfg'
    - '!file_permissions_efi_user_cfg'
    - '!grub2_uefi_password'

    # Following rules are not applicable to RHEL
    - '!package_talk_removed'
    - '!package_talk-server_removed'
