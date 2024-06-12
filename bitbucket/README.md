# About

These are Bitbucket pipeline examples for accomplishing common Snyk workflows. 

**Note:** The default Bitbucket pipeline behavior lookes for a file named `bitbucket-pipeline.yml` in the repository root folder. See the Bitbucket documentation for custom filenames or referencing pipeline files outside the root directory.

### Add Comment To Pull Request With New Vulns and Remediation

#### Option 1: Use Shell Scripts 
Example [bitbucket pipeline yaml](/pipelines/pr-shell-delta-comment.yml)

This pipeline will add a comment to a pull request. The comment will identify newly introduced vulnerabilities and indicate remediation paths
1. Add the example [bitbucket-pipline.yml](/pipelines/pr-shell-delta-comment.yml) to your repository
2. Add the following variables to your repository
    - SECURITY_SCAN
        - Generate this token from Bitbucket's repository access tokens. This token is used to making API requests to Bitbucket. The variable name will be shown as the user in the comment 
    - SNYK_ACCOUNT_TOKEN
        - Generate this token from Snyk. This is used to authenticate snyk scans
    - SNYK_ORG_ID
        - This is the UUID of the organization in Snyk where the baseline scan project exists. You can find this by navigating to the Snyk organization and looking at organization settings.
3. Create a folder in your project called `snyk-tools` with a subfolder called `bin`
4. Copy delta.sh script `snyk-tools/bin` 

#### Option 2: Use a docker image with Snyk tools installed
