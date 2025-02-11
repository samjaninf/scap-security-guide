documentation_complete: true

metadata:
    version: TBD

reference: https://public.cyber.mil/stigs/downloads/?_dl_facet_stigs=operating-systems%2Cunix-linux

title: 'DRAFT - DISA STIG for Oracle Linux 9'

description: |-
    This is a draft profile based on its OL8 version for experimental purposes.
    It is not based on the DISA STIG for OL9, because this one was not available at time of
    the release.

selections:
  - srg_gpos:all
  - var_accounts_authorized_local_users_regex=ol8
