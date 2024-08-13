import os
import re
import subprocess
import config
from modules import snyk_scan


pattern = r'/project/([0-9a-fA-F\-]{36})/'

# Check if the project ID was already added as an environment variable
# If not, do a monitor and grab the project ID

def get_project_id(ci_tool):
    if "BASELINE_PROJECT_ID" in os.environ:
        return os.environ["BASELINE_PROJECT_ID"]
    else:
        if ci_tool == "bitbucket":
            target_branch = config.BITBUCKET_CI_VARS['target_branch']
            pr_branch = config.BITBUCKET_CI_VARS['pr_branch']
        else:
            print("The CI Tool isn't configured")
        
        subprocess.run(['git', 'checkout', os.environ[target_branch]], 
            check=True,  # Raises CalledProcessError on non-zero exit
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True)
        
        print(os.environ[target_branch])
        monitor_stdout = snyk_scan.monitor()
        print(monitor_stdout)

        subprocess.run(['git', 'checkout', os.environ[pr_branch]], 
            check=True,  # Raises CalledProcessError on non-zero exit
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True)
        print(monitor_stdout)
        match = re.search(pattern, monitor_stdout)
        if match:
            return match.group(1)
        else:
            return "No Project ID Found"

