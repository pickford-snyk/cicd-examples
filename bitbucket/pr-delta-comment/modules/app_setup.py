import os
import logging

logger = logging.getLogger(__name__)
environment_variables = ['SNYK_TOKEN', "BASELINE_PROJECT_ID", "BASELINE_ORG_ID"]

def check_token():
    if "SNYK_TOKEN" not in os.environ:
        return logger.error('SNYK_TOKEN is a required environment variable.')

def check_org_id():
    if "BASELINE_ORG_ID" not in os.environ:
        return logger.error('BASELIN_ORG_ID is a required environment variable.')
    
def check_ci_tool():
    # Obviously need to re-write this if we want to handle different tooling
    return "bitbucket"