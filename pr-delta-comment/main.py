import logging
import sys
from modules import app_setup
from modules import snyk_scan
from modules import baseline
from modules import format
from modules import pr_comment_api

logging.basicConfig(
    level=logging.ERROR,  # Set the minimum level of severity to ERROR
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Confirm environment is setup correctly
    app_setup.check_token()
    app_setup.check_org_id()
    app_setup.check_org_slug()
    ci_tool = app_setup.check_ci_tool()

    # Authenticate Snyk CLI
    snyk_scan.auth()
    
    # Run the specified CI delta tests
    concatenated_options = ' '.join(sys.argv[1:])

    #Create an empty list for the comment items
    comment = []
    if len(sys.argv[1:]) > 2:
        print("Options:", sys.argv[1:])
        print("legnth:", len(sys.argv))
        print("Too many arguments. You must pass one option: <test>, <code test>, <os test>, or <iac test>.")
    elif concatenated_options == "test":
        print("Let's check everything!")
        delta = snyk_scan.delta(baseline.get_project_id(ci_tool), "code test")
    elif concatenated_options == "os test":
        # Get the baseline by either running monitor or using config
        delta = snyk_scan.delta("os test")

        # Put the delta data into JSON
        formatted_delta = format.extract_os_issues(delta)

        markdown = format.create_markdown(formatted_delta)

        pr_comment_api.add_comment(ci_tool, markdown)
    elif concatenated_options == "code test":
        print("Let's do a code delta test!")
        delta = snyk_scan.delta(ci_tool, concatenated_options)
        print("delta type: ", type(delta))
        code_issues_json = format.extract_code_issues(delta)
        code_comment_md = format.create_comment_md(code_issues_json, concatenated_options)
        comment.append(code_comment_md)
        print(comment)
    elif concatenated_options == "iac test":
        print("Let's do an iac test!")
        delta = snyk_scan.delta(baseline.get_project_id(ci_tool), "iac test")

    else:
        print("Options:", sys.argv[1:])
        print("Unrecognized options. You must pass one option: <test>, <code test>, <os test>, or <iac test>.")

    markdown = comments
    pr_comment_api.add_comment(ci_tool, markdown)

if __name__ == "__main__":
    main()