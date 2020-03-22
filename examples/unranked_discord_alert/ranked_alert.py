import os
import time

from discord_webhook import DiscordWebhook
from rs2wapy import RS2WebAdmin

# Set this to True to enable this example application.
RUN = False


def get_env_vars(pat: str) -> list:
    i = 1
    env_vars = []
    while True:
        try:
            key = pat.replace("#", str(i))
            env_vars.append(os.environ[key])
            i += 1
        except KeyError:
            break
    return env_vars


# These variables are pulled from the runtime environment,
# don't store passwords or secret information in this file!
WEBADMIN_USERNAMES = get_env_vars("WEBADMIN_USERNAME_#")
WEBADMIN_PASSWORDS = get_env_vars("WEBADMIN_PASSWORD_#")
WEBADMIN_URLS = get_env_vars("WEBADMIN_URL_#")
DISCORD_WEBHOOK_URLS = get_env_vars("DISCORD_WEBHOOK_URL_#")

# Paste the role IDs here that you want to get pinged
# when the unranked alert message is sent.
#
# You may add as many roles as you want (or none), in
# double quotation marks, separated by commas.
#
# For the pings to work the role ID must be of the following format
# <@&ROLE_ID> where ROLE_ID is the role ID you copied from Discord.
PING_DISCORD_ROLES = [
    "<@&111117777888889999>",  # Example role ping, put your real role ID(s) here!
]

# Poll values are in seconds.
# Poll ranked status every 5 seconds.
POLL_INTERVAL = 5
# Alert every 15 minutes if server is unranked.
# The first alert is always sent instantly regardless of this value.
ALERT_INTERVAL = 60 * 15


class Timer:
    """Simple timer class."""

    def __init__(self):
        self._start_time = 0
        self._period = 0

    def start(self, t: float):
        self._start_time = time.time()
        self._period = t

    def expired(self) -> bool:
        return time.time() > (self._start_time + self._period)

    def cancel(self):
        self._start_time = 0
        self._period = 0


def change_map(web_admin: RS2WebAdmin, new_map: str):
    """Change map and wait for change to complete.

    NOTE: If the current map and the new map are the same map,
    this function has no way of knowing if the map change
    was actually successful.
    """
    print(f"Changing map to '{new_map}'", flush=True)

    timed_out = False
    timeout = 60
    start_time = time.time()

    web_admin.change_map(new_map)
    while True and not timed_out:
        timed_out = time.time() > (start_time + timeout)
        try:
            cg = web_admin.get_current_game()
            if cg.info["Map"] == new_map:
                print(f"Map changed successfully", flush=True)
                break
        except Exception as e:
            print(f"WARNING: (non-fatal error): {e}", flush=True)

    if timed_out:
        print("WARNING: timed out while changing maps!", flush=True)


def main():
    web_admins = []

    for wa_uname, wa_pw, wa_url in zip(
            WEBADMIN_USERNAMES, WEBADMIN_PASSWORDS, WEBADMIN_URLS):
        web_admins.append(RS2WebAdmin(
            username=wa_uname,
            password=wa_pw,
            webadmin_url=wa_url,
        ))

    print(f"{len(web_admins)} RS2WebAdmin instances initialized", flush=True)

    # Setup roles we want to ping into a string.
    role_pings = " ".join(PING_DISCORD_ROLES)

    # Setup as many times as we have WebAdmins.
    timers = [Timer() for _ in range(len(web_admins))]

    while True:
        try:
            for wa, wh_url, timer in zip(web_admins, DISCORD_WEBHOOK_URLS, timers):
                # Get server information from WebAdmin.
                cg = wa.get_current_game()
                server_name = cg.info["Server Name"]
                print(f"Polling '{server_name}'", flush=True)

                if not cg.ranked and timer.expired():
                    print(f"'{server_name}' unranked, posting message to Discord", flush=True)

                    # Format our warning message.
                    message = f"Warning, server '{server_name}' is unranked! {role_pings}"

                    # Post the warning message to Discord.
                    webhook = DiscordWebhook(url=wh_url, content=message)
                    webhook.execute()

                    # Start our timer to avoid spamming with alerts.
                    timer.start(ALERT_INTERVAL)

                    # We could also post in game warning message and
                    # change the map automatically.
                    # wa.post_chat_message("SERVER UNRANKED BUG OCCURRED!")
                    # wa.post_chat_message("CHANGING MAP AUTOMATICALLY IN 5 SECONDS!")
                    # time.sleep(5)
                    # change_map(wa, "VNTE-Resort")
                    # If we changed maps automatically, we can just cancel the timer.
                    # timer.cancel()
                    # We could also post an extra warning to Discord.
                    # webhook = DiscordWebhook(url=wh_url, content="Changing map to Resort!")
                    # webhook.execute()

            # Sleep so that poll is performed every POLL_INTERVAL.
            time.sleep(POLL_INTERVAL - time.time() % POLL_INTERVAL)

        except Exception as e:
            print(f"error: {e}, retrying in 15 seconds")
            time.sleep(15)


if __name__ == "__main__":
    if RUN:
        main()
