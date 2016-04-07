from .common import *

from .dockerenv import *

INSTALLED_APPS += ["taiga_contrib_slack"]
# THROTTLING
#REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
#    "anon": "20/min",
#    "user": "200/min",
#    "import-mode": "20/sec"
#}
#LDAP_SERVER = 'ldap://ldap.corp.example.com'
#LDAP_PORT = 389
#
## Full DN of the service account use to connect to LDAP server and search for login user's account entry
## If LDAP_BIND_DN is not specified, or is blank, then an anonymous bind is attempated
##LDAP_BIND_DN = 'CN=SVC Account,OU=Service Accounts,OU=Servers,DC=example,DC=com'
##LDAP_BIND_PASSWORD = 'replace_me'   # eg.
## Starting point within LDAP structure to search for login user
#LDAP_SEARCH_BASE = 'ou=users,dc=example,dc=com'
## LDAP property used for searching, ie. login username needs to match value in sAMAccountName property in LDAP
#LDAP_SEARCH_PROPERTY = 'uid'
#LDAP_SEARCH_SUFFIX = None # '@example.com'
#
## Names of LDAP properties on user account to get email and full name
#LDAP_EMAIL_PROPERTY = 'mail'
#LDAP_FULL_NAME_PROPERTY = 'cn'
