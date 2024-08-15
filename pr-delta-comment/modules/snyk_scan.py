import os
import subprocess

def auth():
    args = []
    args.append('auth')
    args.append(os.environ['SNYK_PR_DELTA'])
    result = subprocess.run(['snyk'] + args, capture_output=True, text=True, shell=False)
    return result.stdout

def monitor():
    args = []
    args.append('monitor')
    # Run the snyk monitor script    
    result = subprocess.run(['snyk'] + args, capture_output=True, text=True, shell=False)
    return result.stdout

def delta(project_id):
    snyk_org = os.environ['SNYK_ORG_ID']
    snyk_test_cmd = ['snyk', 'test', '--json', '--print-deps']
    snyk_delta_cmd = ['snyk-delta', '--baselineOrg', snyk_org, '--baselineProject', project_id]
    scan_output = subprocess.Popen(snyk_test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    delta_stdout = subprocess.Popen(snyk_delta_cmd, stdin=scan_output.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    scan_output.stdout.close()
    
    scan_output.wait()
    delta_stdout.wait()

    delta_output = delta_stdout.communicate()
    
    return delta_output