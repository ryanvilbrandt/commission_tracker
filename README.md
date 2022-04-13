# Quickstart

1. Install Python 3.10+.
2. Install dependencies with `pip install -r requirements.txt`.
3. Add a `SERVICE_ACCOUNT_PASSWORD` environment variable. Can be any value.
4. Create a Google Form for people to use to submit commissions, and have it send the responses to a Google Sheet.
5. Change the Google Sheet's sharing settings so that anyone with the link can **view** it.
6. Add a `SPREADSHEET_ID` environment variable with the ID of the Google Sheet to pull data from.
   1. Example: From the link `https://docs.google.com/spreadsheets/d/aaaBBBcccDDD/edit`, it would be `aaaBBBcccDDD`
7. Create a developer key for Google Sheets and add as a `GOOGLE_SHEETS_DEVELOPER_KEY` environment variable.
   1. See [this page](https://cloud.google.com/docs/authentication/api-keys) for instructions on how to create a developer key. I recommend limiting the scope of the key to Google Sheets.
8. Run `scripts/set_god_password.py` to set up DB and God user.
9. Run `main.py` to start server.
10. Run `run_update_loop.py` to set up background process to keep DB updated with new commissions.