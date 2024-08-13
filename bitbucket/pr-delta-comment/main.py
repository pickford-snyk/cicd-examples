import config
import logging
import subprocess
from modules import app_setup
from modules import snyk_scan
from modules import baseline

logging.basicConfig(
    level=logging.ERROR,  # Set the minimum level of severity to ERROR
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    app_setup.check_token()
    app_setup.check_org_id()
    ci_tool = app_setup.check_ci_tool()
    
    # Authenticate Snyk CLI
    snyk_scan.auth()

    # Get the baseline by either running monitor or using config 
    print(snyk_scan.delta(baseline.get_project_id(ci_tool)))

if __name__ == "__main__":
    main()