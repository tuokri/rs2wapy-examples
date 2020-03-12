import os
import time

from discord_webhook import DiscordWebhook

from rs2wapy import RS2WebAdmin

# Set this to True to enable this example application.
RUN = False

# These variables are pulled from the runtime environment,
# don't store passwords or secret information in this file!
WEBADMIN_USERNAME = os.environ["WEBADMIN_USERNAME"]
WEBADMIN_PASSWORD = os.environ["WEBADMIN_PASSWORD"]
WEBADMIN_URL = os.environ["WEBADMIN_URL"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# Paste the role IDs here that you want to get pinged
# when the unranked alert message is sent.
#
# You may add as many roles as you want (or none), in
# double quotation marks, separated by commas.
#
# For the pings to work the role ID must be of the following format
# <&ROLE_ID> where ROLE_ID is the role ID you copied from Discord.
PING_DISCORD_ROLES = [
    "<&111117777888889999>",  # Example role ping, put your real role ID(s) here!
]

# Poll values are in seconds.
# Poll ranked status every 5 seconds.
POLL_INTERVAL = 5
# Alert every 15 minutes if server is unranked.
ALERT_INTERVAL = 60 * 15


def main():
    wa = RS2WebAdmin(
        username=WEBADMIN_USERNAME,
        password=WEBADMIN_PASSWORD,
        webadmin_url=WEBADMIN_URL,
    )
    print("RS2WebAdmin initialized", flush=True)

    # Setup roles we want to ping into a string.
    role_pings = " ".join(PING_DISCORD_ROLES)

    while True:
        # Get server information from WebAdmin.
        cg = wa.get_current_game()
        server_name = cg.info["Server Name"]

        if not cg.ranked:
            print("Server unranked, posting message to Discord", flush=True)

            # Format our warning message.
            message = f"Warning, server '{server_name}' is unranked! {role_pings}"

            # Post the warning message to Discord.
            webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
            webhook.execute()

        # Sleep so that poll is performed every POLL_INTERVAL.
        time.sleep(POLL_INTERVAL - time.time() % POLL_INTERVAL)


if __name__ == "__main__":
    if RUN:
        main()
