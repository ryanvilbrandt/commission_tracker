# Quickstart

## Ko-fi

### Basic Server Setup

1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `scripts/set_god_password.py` to set up DB and God user.
   1. You can create a `users.csv` file in the `scripts` directory to automate the creation of the God user and any other users when you run this script. Use the `users.csv.dist` file as a template.
4. Run `main.py` to start the server.

### Integrating with Ko-fi

The following instructions assume you have a domain that can be used to hit the machine you're using to run Commission Tracker.

1. Edit conf/config.ini
   1. Change the `host` value to the local IP of the machine Commission Tracker is running on.
   2. Set `port` to whatever value you want. Set it to port 80 if you want users to hit the Commissions Tracker without having to specify a port in their URL.
2. Go to the [Ko-fi webhooks](https://ko-fi.com/manage/webhooks) page and set `{domain}/kofi_webhook` as the webhook URL, where `{domain}` is the domain you have set up for your machine.
3. Add a `KOFI_VERIFICATION_TOKEN` environment variable using the verification token provided by the Ko-fi webhooks page, under the `Advanced` accordion.
4. Stop `main.py` if it's running, and start it again.
   1. On Windows, you may need to logout and back in for your environment variable change to take effect.
5. Use the "Test a webhook" buttons on the Ko-fi webhook page. You should see a commission appear on the Commission Tracker. 

You can also use the `scripts/test_kofi_webhook.py` script to push 

## Google Sheets

_Note:_ This method has been disabled in this version of the Commission Tracker. Use the Ko-fi setup above.

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