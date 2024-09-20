import re
import json
import os
from modules import baseline
from modules import app_setup

# Unlike the Code and IaC delta tool, Snyk OS delta tool doesn't produce JSON. Most of the formatting methods convert
# stdout from the snyk-delta tool into formatted JSON

# This markdown wraps the content from individual product findings
def create_comment_md(json_issues, type):
    org_slug = os.environ["SNYK_ORG_SLUG"]
    if type != "code test":
        project_id = baseline.get_project_id(app_setup.check_ci_tool())
        snyk_project_url = "https://app.snyk.io/org/" + org_slug + "/project/" + project_id
    else:
        snyk_project_url = "https://app.snyk.io/org/" + org_slug

    color_codes = {
        "Critical Severity": "&#128308; Critical", # Red
        "High Severity": "&#128308; High",  # Red
        "Medium Severity": "&#127464; Medium", # Yellow
        "Low Severity": "&#9898; Low"    # Gray
    }

    # Snyk branding in the comment header
    markdown = "![Snyk Header Image](https://camo.githubusercontent.com/d5c338bf6ef2b50e56a8092a3b4ccbc82655bd86d2845d2984572c0b91b60b51/68747470733a2f2f7265732e636c6f7564696e6172792e636f6d2f736e796b2f696d6167652f75706c6f61642f722d642f73636d2d706c6174666f726d2f736e796b2d70756c6c2d72657175657374732f70722d62616e6e65722d64656661756c742e737667)\n\n"

    # Table of issues
    if json_issues:
        if type == "os test":
            markdown = create_os_md(markdown, json_issues, color_codes)
        elif type == "code test":
            markdown = create_code_md(markdown, json_issues, color_codes)
        elif type == "iac test":
            markdown = create_iac_md(markdown, json_issues, color_codes)
        elif type == "test":
            print("Still need to work on multi-product")

    else:
        markdown += "# :tada: No new issues found!\n\n"

    markdown += "\n\n"
    markdown += "## &#128269; View [this project](" + snyk_project_url + ") in Snyk."
    return markdown

def create_os_md(markdown, json_data, color_codes):
    markdown += "# &#10071;&#10071; OS Issues found!\n"
    markdown += "## Issue Summary\n\n"
    markdown += "| Type | ID | Description | Severity | CVSS Score | Fixed In | Upgrade Path |\n"
    markdown += "|----|----|-------|----------|------------|----------|-----|\n"

    for issue in json_data:
        severity = color_codes.get(issue['severity'], "Unknown")
        description = issue['description'] if issue['description'] is not None else "N/A"
        cvss_score = issue['cvssScore'] if issue['cvssScore'] is not None else "N/A"
        fixed_in = issue['fixed_in'] if issue['fixed_in'] is not None else "N/A"
        upgrade_path = issue['upgrade_path'] if issue['upgrade_path'] is not None else "No known upgrade path"

        markdown += f"| {issue['type']} | {issue['issue_id']} | {description} | {severity} | {cvss_score} | {fixed_in} | {upgrade_path} |\n"
        markdown += "\n\n"
    return os_md

# Create the markdown for the Code Scan delta
def create_code_md(markdown, json_data, color_codes):

    markdown += "# &#10071;&#10071; Code Issues found!\n"
    markdown += "## Issue Summary\n\n"
    markdown += "| Type | ID | Description | Severity | Priority Score | Location |\n"
    markdown += "|----|----|-------|----------|------------|----------|\n"

    for issue in json_data:
        severity = color_codes.get(issue['severity'], "Unknown")
        description = issue['description'] if issue['description'] is not None else "N/A"
        cvss_score = issue['cvssScore'] if issue['cvssScore'] is not None else "N/A"
        fixed_in = issue['fixed_in'] if issue['fixed_in'] is not None else "N/A"

    markdown += f"| {issue['type']} | {issue['issue_id']} | {description} | {severity} | {cvss_score} | {location} |\n"
    markdown += "\n\n"

    return code_md

def create_iac_md(markdown, json_data):
    markdown += "# &#10071;&#10071; IaC Issues found!\n"
    markdown += "## Issue Summary\n\n"
    markdown += "| Type | ID | Description | Severity | CVSS Score | Fixed In |\n"
    markdown += "|----|----|-------|----------|------------|----------|\n"

    for issue in json_data:
        severity = color_codes.get(issue['severity'], "Unknown")
        description = issue['description'] if issue['description'] is not None else "N/A"
        cvss_score = issue['cvssScore'] if issue['cvssScore'] is not None else "N/A"
        fixed_in = issue['fixed_in'] if issue['fixed_in'] is not None else "N/A"

    markdown += f"| {issue['type']} | {issue['issue_id']} | {description} | {severity} | {cvss_score} | {fixed_in} |\n"
    markdown += "\n\n"
    return iac_md

def extract_os_issues(delta):
    delta_string = delta[0]
    pattern = '_____________________________'
    last_index = delta_string.rfind(pattern)
    start_index = last_index + len(pattern)
    json_delta = create_os_json(delta_string[start_index:].strip())

    return json_delta

def extract_code_issues(delta):
    delta_json = json.loads(delta)
    issues = delta_json.get('results')
    code_issues_json = '''
    {
        "issues": []
    }
    '''
    for issue in issues:
        # Create an empty dict for the data we're collecting
        issue_data = {
            'description': '',
            'severity': '',
            'priority_score': '',
            'autoFix': '',
            'location': []
        }

        # Find the data in the delta and add it to the dict. Normalize the severity data
        description = issue['message'].get('text')
        issue_data['description'] = description
        level = issue.get('level')
        if level == "error":
            issue_data['severity'] = "High Severity"
        elif level == "warn":
            issue_data['severity'] = "Medium Severity"
        elif level == "note":
            issue_data['severity'] = "Low Severity"
        else:
            issue_data['severity'] = "N/A"
        autoFix = issue['properties'].get('isAutofixable')
        issue_data['autoFix'] = autoFix
        score = issue['properties'].get('priorityScore')
        issue_data['priority_score'] = score
        location = issue['locations']
        issue_data['location'] = location

        # convert our JSON to a dict, add the new data, convert back to JSON string
        code_issues_dict = json.loads(code_issues_json)
        code_issues_dict['issues'].append(issue_data)
        code_issues_json = json.dumps(code_issues_dict, indent=4)
        print("JSON object:\n", code_issues_json)

    return code_issues_json

def create_os_json(stdout_delta):
    
    vulnerabilities = []

    if "No new issues found !" not in stdout_delta:
        # Split the text into lines
        sections = stdout_delta.strip().split('New issue introduced !\n')
        sections = filter(None, sections)
        
        for section in sections:
            lines = section.strip().split('\n')

            # Extract issue details from the lines
            issue_type = lines[0].strip(':\n')
            issue_id = extract_issue_id(lines[2])
            description = extract_description(lines[2])
            issue_info = lines[2].strip()
            via_info = lines[3].strip() if len(lines) > 3 else ''
            fixed_in_info = lines[4].strip() if len(lines) > 4 else ''
            fixable_by_info = lines[5].strip() if len(lines) > 5 else ''

            # Create a dictionary for the current issue
            issue_data = {
                "type": issue_type,
                "issue_id": issue_id,
                "description": description,
                "severity": issue_info.split('[')[1].split(']')[0].strip(),
                "cvssScore": issue_info.split('cvssScore: ')[1].split(']')[0].strip() if 'cvssScore' in issue_info else None,
                "via": via_info.split(':')[1].strip() if 'Via' in via_info else None,
                "fixed_in": fixed_in_info.split(':')[1].strip() if 'Fixed in' in fixed_in_info else None,
                "upgrade_path": fixable_by_info.split(':')[1].strip() if 'Fixable by upgrade' in fixable_by_info else None
            }
        
            vulnerabilities.append(issue_data)

    return vulnerabilities




def extract_description(line):
    # Find the start and end positions of the description
    start_marker = ':'
    end_marker = '['

    # Match the pattern of security vulns (rather than license vulns)
    pattern = r':[a-zA-Z].*?\s\['    
    if re.search(pattern, line):
        start_pos = line.find(start_marker, line.find(start_marker) + 1) + 1
        if start_pos == -1:
            return None

        # Find the end of the description
        end_pos = line.find(end_marker, start_pos)
        if end_pos == -1:
            end_pos = len(line)

        # Extract the description
        description = line[start_pos:end_pos].strip()
    else:
        description = None
    return description

def extract_issue_id(line):
    # Snyk OS ID pattern:
    pattern = r'/[1-9]:\s([A-Z0-9-\.]*(\slicense)?)'
    
    # Search for each pattern
    match = re.search(pattern, line)
    dirty_issue_id = match.group(1)

    pattern2 = r'\d+/\d+: '

    issue_id = re.sub(pattern2, '', dirty_issue_id) 

    return issue_id

