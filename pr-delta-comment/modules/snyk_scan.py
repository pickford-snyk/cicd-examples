import os
import json
import subprocess
from modules import baseline

def auth():
    args = []
    args.append('auth')
    args.append(os.environ['SNYK_TOKEN'])
    result = subprocess.run(['snyk'] + args, capture_output=True, text=True, shell=False)
    return result.stdout

def monitor():
    args = []
    args.append('monitor')
    # Run the snyk monitor script    
    result = subprocess.run(['snyk'] + args, capture_output=True, text=True, shell=False)
    return result.stdout

def delta(ci_tool, type):
    if type == "os":
        snyk_org = os.environ['SNYK_ORG_ID']
        os_delta(snyk_org, ci_tool)
    elif type == "code test":
        delta = code_delta(ci_tool)
        return delta
    elif type == "iac test":
        iac_delta(ci_tool)
    elif type == "test":
        snyk_org = os.environ['SNYK_ORG_ID']
        multiple_products = []
        multiple_products.append(os_delta(snyk_org, ci_tool))
        multiple_products.append(code_delta(ci_tool))
        multiple_products.append(iac_delta(ci_tool))
    else:
        return "Invalid option"


def os_delta(snyk_org, ci_tool):
    project_id = delta(baseline.get_os_baseline(ci_tool))
    snyk_test_cmd = ['snyk', 'test', '--json', '--print-deps']
    snyk_delta_cmd = ['snyk-delta', '--baselineOrg', snyk_org, '--baselineProject', project_id]
    scan_output = subprocess.Popen(snyk_test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    delta_stdout = subprocess.Popen(snyk_delta_cmd, stdin=scan_output.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    scan_output.stdout.close()
    
    scan_output.wait()
    delta_stdout.wait()

    delta_output = delta_stdout.communicate()
    
    return delta_output

def code_test(type):
    if type == 'baseline':
        code_json_cmd = ['snyk', 'code', 'test', "--json-file-output=baseline.json"]
        subprocess.Popen(code_json_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).wait()
        pass
    elif type == 'new':
        code_json_cmd = ['snyk', 'code', 'test', "--json-file-output=new.json"]
        subprocess.Popen(code_json_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).wait()
        pass

def code_delta(ci_tool):
    # Create the baseline JSON from the target branch
    baseline.get_code_baseline(ci_tool)
    # Test the new code
    code_test('new')
    code_delta_cmd = ['/Users/opickford/snyk_tools/snyk-code-iac-delta', 'code', 'baseline.json', 'new.json']
    # The code / iac delta tool creates another JSON file
    subprocess.Popen(code_delta_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).wait()
    with open('./snyk_pr_diff_scan.json', 'r') as file:
        code_delta_json = file.read()

    return code_delta_json

def iac_test(type):
    if type == 'baseline':
        snyk_iac_test_cmd = ['snyk', 'iac', 'test', "--json-file-output=baseline.json"]
        subprocess.Popen(snyk_iac_test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).wait()
        pass
    elif type == 'new':
        snyk_iac_test_cmd = ['snyk', 'iac', 'test', "--json-file-output=new.json"]
        subprocess.Popen(snyk_iac_test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).wait()
        pass

def iac_delta():
    baseline = baseline.get_iac_baseline()
    pr = iac_test()
    snyk_test_cmd = ['snyk-code-iac-delta', 'code', baseline, pr]

    return snyk_test_cmd