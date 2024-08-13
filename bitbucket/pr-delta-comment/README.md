User Instructions
1. Add the SNYK_TOKEN as an environment variable
2. Add the SNYK Org UUID as an environment variable

Oprtional
1. Add the project ID as an environment variable


-------

App Steps
1. Create baseline with Snyk monitor 
    - need both a project ID and an org ID
    - potentially check for existing baseline
2. Snyk delta from passing in baseline
3. 

To Dos
- Move local snyk-tools into app
    CURRENT STATUS:
    - trying to do a snyk scan from the python app and it's not authenticating correctly. Need to check what arguments are being passed to the snyk command

- run python scrips with unique commands from bitbucket-pipelines.yml
- Potential improvement here might be to get the Org ID using the API, rather than requiring users to add it as an environment variable