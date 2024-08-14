# CI Tools Configs
BITBUCKET_CI_VARS = {
    'target_branch': 'BITBUCKET_PR_DESTINATION_BRANCH',
    'pr_branch': "BITBUCKET_BRANCH",
}

BITBUCKET_PR_COMMENT_API = {
    'api_base_url': 'https://api.bitbucket.org/2.0/repositories/',
    'variable_1': '$BITBUCKET_WORKSPACE',
    'path_1': '/',
    'variable_2': '$BITBUCKET_REPO_SLUG',
    'path_2': '/pullrequests/',
    'variable_3': '$BITBUCKET_PR_ID',
    'path_3': '/comments'
}