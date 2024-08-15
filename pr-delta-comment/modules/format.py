import re
import json

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
    # Split the text into lines

    sections = stdout_delta.strip().split('New issue introduced !\n')
    sections = filter(None, sections)
    
    vulnerabilities = []

    for section in sections:
        lines = section.strip().split('\n')

        # Extract issue details from the lines
        issue_type = lines[0].strip()
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
    
    # Convert the list of dictionaries to a JSON object
    json_object = json.dumps(vulnerabilities, indent=4)
    
    return json_object

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