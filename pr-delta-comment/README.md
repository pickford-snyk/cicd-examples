### Overview
Use this application to generage a pull request common for any new vulnerabilities
introduced from a pull request.

User Instructions
1. Use the [docker image](https://hub.docker.com/repository/docker/opickford/pr-delta-comment/general) to your build pipeline. Eg:
```image: opickford/pr-delta-comment:latest```
2. Use a token with appropriate permission to set a `SNYK_TOKEN` environment variable.
3. Add a `SNYK_ORG_ID` environment variable with the value of the Snyk organization you want to use.

Optional
1. Add the project ID as an environment variable. This will skip the build step that creates a project in Snyk, potentially saving some time.


-------

Limitations & Improvements
- Add Snyk Code, Container and IaC scan deltas
- New commits do not trigger PR comment update
- Get Org ID using the API, rather than requiring users to add it as an environment variable
- Configure CI tools other than bitbucket in the config.py file