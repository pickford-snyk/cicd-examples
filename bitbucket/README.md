# About

Bitbucket pipeline examples for accomplishing common Snyk workflows

## Pull Requests

### Adding a comment with remediation for newly introduced vulnerablities 

#### Add the example [bitbucket-pipline.yml](bitbucket-pipeline) to your repository
#### Add the following variables to your repository
##### SECURITY_SCAN_COMMENT: Generate this token from Bitbucket's repository access tokens. This token is used to making API requests to Bitbucket. The variable name will be shown as the user in the comment 
##### SNYK_TOKEN: Generate this token from Snyk. This is used to authenticate snyk scans
