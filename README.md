# Quickstart

## Ko-fi

### Basic Server Setup

1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `scripts/set_god_password.py` to set up DB and God user.
   1. You can create a `users.csv` file in the `scripts` directory to automate the creation of the God user and any other users when you run this script. Use the `users.csv.dist` file as a template.
4. Run `main.py` to start the server.

### Windows Batch Helpers

There are several .bat files provided to automate or simplify working with this software.
1. `install.bat` - Performs a full installation in the root folder of the software utilizing a virtual environment.
2. `bat/add_fake_comms.bat` - Sends 5 fake commissions to the server.
3. `bat/setup_users.bat` - Runs `set_god_password.py`. Helpful if you draft `users.csv` prior.
4. `bat/start_server.bat` - Starts the server, simple as that.
5. `bat/priv/run.bat` - Runs a single line of batch in the virtual environment set up by `install.bat`.
6. `bat/priv/run_with_token.bat` - Identical to `run.bat`, with the addition of `KOFI_VERIFICATION_TOKEN` being set in the environment.

Both `add_fake_comms.bat` and `start_server.bat` require that you populate `bat/priv/kofi_verification_token.txt` with your Ko-fi token. This is detailed in the following section.

### Integrating with Ko-fi

The following instructions assume you have a domain that can be used to hit the machine you're using to run Commission Tracker, and have configured your network to allow it to be hit from the public internet.

1. Edit conf/config.ini
   1. Change the `host` value to the local IP of the machine Commission Tracker is running on.
   2. Set `port` to whatever value you want. Set it to port 80 if you want users to hit the Commissions Tracker without having to specify a port in their URL.
2. Go to the [Ko-fi webhooks](https://ko-fi.com/manage/webhooks) page and set `{domain}/kofi_webhook` as the webhook URL, where `{domain}` is the domain you have set up for your machine.
3. Add a `KOFI_VERIFICATION_TOKEN` environment variable using the verification token provided by the Ko-fi webhooks page, under the `Advanced` accordion.
4. Stop `main.py` if it's running, and start it again.
   1. On Windows, you may need to logout and back in for your environment variable change to take effect.
5. Use the "Test a webhook" buttons on the Ko-fi webhook page. You should see a commission appear on the Commission Tracker. 

You can also use the `scripts/test_kofi_webhook.py` script to make randomized calls to your webhook.

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

# TODO

* Add email field to commissions and an "Update Email" button for quick updates of the data
* Add "Update name" button to commissions
* Add Archive button
* Add undo Archive/Email/Refund buttons.
* Add Export Images option. Group images by commissioner name/email
* Add sorting options for the user:
  * Updated TS
  * Email
  * Username
  * Created TS
  * Commission ID
* Add ability to visually group commissions together by user
* Add "unclick" admin buttons for emailed and refunded
* Look into hooking Queue Open/Close to the Twitch Overlay
* Add tracking for which users have websockets open
* Figure out way to make multiple actions in a row bog things down less.
  * I think bottle is single-threaded, so may not be able to manage multiple threads.
  * Switch to pushing updates over the websocket itself? Could be single-threaded that way.
  * Figure out if bottle can be multi-threaded. If so, create threading.lock when writing.