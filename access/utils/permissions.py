from core.miniframework_on_django.query_layer.access_query.permission import PermissionIssueChecker, \
    PermissionLevelChecker


class SignUpPermissionChecker(PermissionIssueChecker):
    issue = 'sign-up'


class CompanyClientPermissionChecker(PermissionLevelChecker):
    level = 'company_client'
