# CAELUS_GroundInfrastructure

# Dependencies
To install the required dependencies issue `pip3 install -r requirements.txt`.

# Credentials setup
To avoid pushing sensitive data to the GitHub repo, this project makes use of .env files for tests.
Create a `.env.test` file in the root directory of the project.
The file must contain the authentication information for the test accounts (CVMS and DIS).

Here's an example `.env.test` file:

```
DIS_GRANT_TYPE=<grant_type>
DIS_CLIENT_ID=<client_id>
DIS_USERNAME=<your_username>
DIS_PASSWORD=<your_password>
```

# Running tests
From the project's root folder, issue `python3 -m pytest`.