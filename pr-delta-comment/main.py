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
    if len(sys.argv) > 2:
        print("You must pass one option: <test>, <code test>, <os test>, or <iac test>.")
    elif sys.argv == "test":
        print("Let's check everything!")
    elif sys.argv == "code test":
        print("Let's do a code test!")
    elif sys.argv == "iac test":
        print("Let's do an iac test!")
    elif sys.argv == "os test":
        # Get the baseline by either running monitor or using config 
        delta = snyk_scan.delta(baseline.get_project_id(ci_tool))

        # Put the delta data into JSON
        formatted_delta = format.extract_vulns(delta)

        markdown = format.create_markdown(formatted_delta)

        pr_comment_api.add_comment(ci_tool, markdown)
    else:
        print("You must pass one option: <test>, <code test>, <os test>, or <iac test>.")

if __name__ == "__main__":
    main()