# Security Policy

## Supported Version

This is a portfolio project. The current supported baseline is:

    v0.1.0

## Secrets

Do not commit secrets to the repository.

Never commit:

- `.env`
- `.streamlit/secrets.toml`
- API keys
- Access tokens
- Private grant documents
- Private applicant data
- Real funder credentials

Use local environment variables, `.env`, or Streamlit Community Cloud secrets for runtime configuration.

## Expected Local Secret Files

Local files that may contain secrets are ignored by Git:

    .env
    .streamlit/secrets.toml

The repository includes examples only:

    .env.example
    .streamlit/secrets.toml.example

## OpenAI API Key

The OpenAI API key should be provided through one of these mechanisms:

- Shell environment variable
- Local `.env` file
- Streamlit Community Cloud secrets

The app should not print or display the API key value.

## Uploaded Documents

The app is intended for local or controlled demo usage. Do not upload private, confidential, regulated, or client-owned grant materials into a public deployment unless the deployment environment, storage behavior, access controls, and data-handling process have been reviewed.

## Reporting Issues

For portfolio review, open a GitHub issue describing:

- The issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Any relevant traceback without secrets
