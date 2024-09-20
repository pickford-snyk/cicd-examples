import os
import re
import subprocess
import config
from modules import snyk_scan

# This is the URL pattern for identifying Snyk project IDs
pattern = r'/project/([0-9a-fA-F\-]{36})/'

def get_environment_baselines():
    baseline_ids = {
        'os_baseline': '',
        'code_baseline': '',
        'iac_baseline': ''
    }
    # Check if the Project is in already in Snyk and Configured as an Environment Variable
    if "OS_BASELINE_PROJECT_ID" in os.environ:
        baseline_ids['os_baseline'] = os.environ["OS_BASELINE_PROJECT_ID"]
    # If the project baseline isn't configured, do a scan to create a baseline from the target branch
    if "CODE_BASELINE_PROJECT_ID" in os.environ:
        baseline_ids['code_baseline'] = os.environ["CODE_BASELINE_PROJECT_ID"]
    if "IAC_BASELINE_PROJECT_ID" in os.environ:
        baseline_ids['iac_baseline'] = os.environ["IAC_BASELINE_PROJECT_ID"]
    return baseline_ids

def get_os_baseline(ci_tool):
    baselines = get_environment_baselines()
    if baselines['os_baseline'] != '':
        project_id = baselines['os_baseline']
        return project_id
    else:
        branches = get_branches(ci_tool)
        # Check out the target branch
        subprocess.run(['git', 'checkout', os.environ[branches[0]]],
            check=True,  # Raises CalledProcessError on non-zero exit
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True)

        # Crete a baseline scan and capture the monitor output to get the project ID
        monitor_stdout = snyk_scan.monitor()

        # Check the PR branch back out
        subprocess.run(['git', 'checkout', os.environ[branches[1]]],
            check=True,  # Raises CalledProcessError on non-zero exit
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True)
        match = re.search(pattern, monitor_stdout)
        if match:
            os.environ['BASELINE_PROJECT_ID'] = match.group(1)
            return match.group(1)
        else:
            return "No Project ID Found"

def get_code_baseline(ci_tool):
    baselines = get_environment_baselines()
    if baselines['code_baseline'] != '':

        # NOTE: This doesn't work yet. To handle pre-set project, the tool will need to create a json file that the
        # delta tool can handle. Request the project issues from snyk, then create a method to generate a file matching
        # the output generated from the snyk code delta tool
        #
        # Example:
        # project_id = baselines['code_baseline']
        # snyk_api_token = os.environ['SNYK_TOKEN']
        # snyk_org = os.environ['SNYK_ORG_ID']
        # snyk_api_output = request_snyk_project(snyk_api_token, snyk_org, project_id)
        # create_baseline_json_file(snyk_api_output)

        print("code baseline isn't configured")
        pass
    else:
        branches = get_branches(ci_tool)
        print(branches[0])
        subprocess.run(['git', 'checkout', branches[0]],
            check=True,  # Raises CalledProcessError on non-zero exit
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)
        snyk_scan.code_test('baseline')
        subprocess.run(['git', 'checkout', branches[1]],
            check=True,  # Raises CalledProcessError on non-zero exit
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)
        pass

def get_iac_baseline():
    baselines = get_environment_baselines()
    if baselines['iac_baseline'] != '':

        # NOTE: This doesn't work yet. To handle pre-set project, the tool will need to create a json file that the
        # delta tool can handle. Request the project issues from snyk, then create a method to generate a file matching
        # the output generated from the snyk code delta tool
        #
        # Example:
        # project_id = baselines['code_baseline']
        # snyk_api_token = os.environ['SNYK_TOKEN']
        # snyk_org = os.environ['SNYK_ORG_ID']
        # snyk_api_output = request_snyk_project(snyk_api_token, snyk_org, project_id)
        # create_baseline_json_file(snyk_api_output)

        print("iac baseline isn't configured")
        pass
    else:
        branches = get_branches("bitbucket")
        subprocess.run(['git', 'checkout', branches[0]], check=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        snyk_scan.iac_test('baseline')
        subprocess.run(['git', 'checkout', branches[1]], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pass

def get_branches(ci_tool):
    if ci_tool == "bitbucket":
        branches = []
        target_branch = config.BITBUCKET_CI_VARS['target_branch']
        branches.append(os.environ[target_branch])
        pr_branch = config.BITBUCKET_CI_VARS['pr_branch']
        branches.append(os.environ[pr_branch])
    else:
        print("The CI Tool isn't configured")
        branches = []
    return branches