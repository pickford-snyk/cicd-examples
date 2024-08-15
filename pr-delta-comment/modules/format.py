import re
import json
import os
from modules import baseline
from modules import app_setup

# All this logic is largely necessary because we don't have formatted delta
# The current snyk-delta tool just provides an stdout that has to be formatted
# in order to work with the data for API requests 


def extract_vulns(delta):
    delta_string = delta[0]
    pattern = '_____________________________'
    last_index = delta_string.rfind(pattern)
    start_index = last_index + len(pattern)
    json_delta = create_json(delta_string[start_index:].strip())

    return json_delta

def create_json(stdout_delta):
    
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

def create_markdown(json_data):
    org_slug = os.environ["SNYK_ORG_SLUG"]
    project_id = baseline.get_project_id(app_setup.check_ci_tool())
    snyk_project_url = "https://app.snyk.io/org/" + org_slug + "/project/" + project_id

    # Define color codes for severity
    color_codes = {
        "Critical Severity": "<span style='display: inline-block; width: 20px; height: 20px; background-color: #ad1a1a; border-radius: 50%;'></span> Critical", # Red
        "High Severity": "<span style='display: inline-block; width: 20px; height: 20px; background-color: #cc4f19; border-radius: 50%;'></span> High",  # Red
        "Medium Severity": "<span style='display: inline-block; width: 20px; height: 20px; background-color: #d68100; border-radius: 50%;'></span> Medium", # Orange
        "Low Severity": "<span style='display: inline-block; width: 20px; height: 20px; background-color: #86859d; border-radius: 50%;'></span> Low"    # Yellow
    }
    
    markdown = "![Snyk Header Image](https://camo.githubusercontent.com/d5c338bf6ef2b50e56a8092a3b4ccbc82655bd86d2845d2984572c0b91b60b51/68747470733a2f2f7265732e636c6f7564696e6172792e636f6d2f736e796b2f696d6167652f75706c6f61642f722d642f73636d2d706c6174666f726d2f736e796b2d70756c6c2d72657175657374732f70722d62616e6e65722d64656661756c742e737667)\n\n"
    
    if json_data:
        markdown += "# &#10071;&#10071; Snyk Found New Issues\n"
        markdown += "## Issue Summary\n\n"
        markdown += "| Type | ID | Description | Severity | CVSS Score | Fixed In | Upgrade Path |\n"
        markdown += "|----|----|-------|----------|------------|----------|-----|\n"

        # Add rows for each 
        for issue in json_data:
            severity = color_codes.get(issue['severity'], "Unknown")
            description = issue['description'] if issue['description'] is not None else "N/A"
            cvss_score = issue['cvssScore'] if issue['cvssScore'] is not None else "N/A"
            fixed_in = issue['fixed_in'] if issue['fixed_in'] is not None else "N/A"
            upgrade_path = issue['upgrade_path'] if issue['upgrade_path'] is not None else "No known upgrade path"
            
            markdown += f"| {issue['type']} | {issue['issue_id']} | {description} | {severity} | {cvss_score} | {fixed_in} | {upgrade_path} |\n"
    else:
        markdown += "# :tada: No new vulns found\n\n"
    
    markdown += "\n\n"
    markdown += "&#128269; View this projects scans in [Snyk](" + snyk_project_url + ")"
    return markdown

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