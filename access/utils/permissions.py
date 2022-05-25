from core.miniframework_on_django.query_layer.access_query.permission import PermissionIssueChecker, \
    PermissionLevelChecker


class SignUpPermissionChecker(PermissionIssueChecker):
    issue = 'sign-up'


class LoginPermissionChecker(PermissionIssueChecker):
    issue = 'login'


class FindingPasswordPermissionChecker(PermissionIssueChecker):
    issue = 'finding-password'


class CompanyClientPermissionChecker(PermissionLevelChecker):
    level = 'company_client'


class AdminPermissionChecker(PermissionLevelChecker):
    level = 'admin'


USER_LEVEL_MAP = {
    0: 'admin',
    1: 'company_client',
    2: 'client',
}
