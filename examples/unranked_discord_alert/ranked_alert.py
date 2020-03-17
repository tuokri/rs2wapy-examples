import os
import time

from discord_webhook import DiscordWebhook
from rs2wapy import RS2WebAdmin

# Set this to True to enable this example application.
RUN = True


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
WEBADMIN_USERNAMES = os.environ["WEBADMIN_USERNAME"]
WEBADMIN_PASSWORDS = os.environ["WEBADMIN_PASSWORD"]
WEBADMIN_URLS = os.environ["WEBADMIN_URL"]
DISCORD_WEBHOOK_URLS = os.environ["DISCORD_WEBHOOK_URL"]

# Paste the role IDs here that you want to get pinged
# when the unranked alert message is sent.
#
# You may add as many roles as you want (or none), in
# double quotation marks, separated by commas.
#
# For the pings to work the role ID must be of the following format
# <&ROLE_ID> where ROLE_ID is the role ID you copied from Discord.
PING_DISCORD_ROLES = [
    "<@&552280559284650016>",  # Example role ping, put your real role ID(s) here!
]

# Poll values are in seconds.
# Poll ranked status every 5 seconds.
POLL_INTERVAL = 5

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

    switching = False
    while True:
        try:
            for wa, wh_url in zip(web_admins, DISCORD_WEBHOOK_URLS):
                # Get server information from WebAdmin.
                cg = wa.get_current_game()
                server_name = cg.info["Server Name"]
                
                if switching:
                    cg = wa.get_current_game()
                    if cg.info["Map"].lower() == "vnte-cuchi":
                        print("Map changed succesfully!")
                        switching = False
                
                if not cg.ranked and not switching:
                    print(f"'{server_name}' unranked, posting message to Discord", flush=True)

                    # Format our warning message.
                    message = f"SERVER UNRANKED, SWITCHING TO CU CHI! {role_pings}"
                    wa.post_chat_message("SERVER BUG! NOBODY CAN JOIN! Changing maps!")
                    wa.post_chat_message("SERVER BUG! NOBODY CAN JOIN! Changing maps!")
                    wa.post_chat_message("SERVER BUG! NOBODY CAN JOIN! Changing maps!")
                    wa.post_chat_message("SERVER BUG! NOBODY CAN JOIN! Changing maps!")
                    wa.post_chat_message("SERVER BUG! NOBODY CAN JOIN! Changing maps!")
                    wa.post_chat_message("SERVER BUG! NOBODY CAN JOIN! Changing maps!")
                    wa.post_chat_message("SERVER BUG! NOBODY CAN JOIN! Changing maps!")
                    time.sleep(10)
                    wa.change_map("VNTE-Cuchi")
                    # Post the warning message to Discord.
                    webhook = DiscordWebhook(url=wh_url, content=message)
                    webhook.execute()
                    switching = True

            # Sleep so that poll is performed every POLL_INTERVAL.
            time.sleep(POLL_INTERVAL - time.time() % POLL_INTERVAL)

        except Exception as e:
            print(f"error: {e}, retrying in 15 seconds")
            time.sleep(15)


if __name__ == "__main__":
    if RUN:
        main()

