# Snyk PR Delta Comment

### Overview
Use this application to identify new issues introduced in pull requests.

Usage Instructions
1. Use the [docker image](https://hub.docker.com/repository/docker/opickford/pr-delta-comment/general) to your build pipeline. Eg:
```image: opickford/pr-delta-comment:latest```
2. Provision a Snyk token with appropriate permissions and `SNYK_TOKEN` environment variable with the token value.
3. Add a `SNYK_ORG_ID` environment variable with the value of the Snyk organization you want to use.
4. Add a `SNYK_ORG_SLUG` environment variable with the value of the Snyk organization you want to use.
5. Provision an SCM token with permissions to make comments and add it as repository variable with the name `SNYK_PR_DELTA`.
4. Invoke the app by running `snyk-pr-delta-comment`

Example Pipeline Files
- [Bitbucket](../bitbucket/pipeline-examples/pr-comment-delta-docker.yml)

-------

Limitations & Future Improvements
- Allow adding the project ID as an environment variable, skipping step that creates a project in Snyk
- Add Snyk Code, Container and IaC scan deltas
- New commits do not trigger PR comment update
- Get Org ID using the API, rather than requiring users to add it as an environment variable
- Configure CI tools other than bitbucket in the config.py file