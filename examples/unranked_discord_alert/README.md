# Discord Unranked Alert Example Application

This example application sends a message to Discord when the RS2
server goes unranked. Server ranked status is checked every 5 seconds.
If the server is unranked, the first message is sent instantly and
after that a message is sent every 15 minutes until the server is ranked again.

Make sure you read [the general example README](../../README.md) first.

There are unlimited ways to deploy applications using `rs2wapy`.
This particular example uses [Heroku](https://www.heroku.com/)
to host the unranked alert bot.

You may also read this guide at [RS2 Community Hub](https://steamcommunity.com/sharedfiles/filedetails/?id=2031260172).

### Directory Structure
Brief explanation of the files in this directory.
```
ranked_alert.py  # example application source code
README.md        # this readme file
```

### Instructions
Detailed steps on setting up this example application.

#### 1. Setting up GitHub
1. Create a GitHub account at https://github.com/join.

2. Fork this example repository https://github.com/tuokri/rs2wapy-examples.
    
    ![Fork Examples](../images/github_fork_examples.png)
    
    After forking, you will have a copy of this repository
    in your GitHub account.

#### 2. Setting up Heroku
1. Create a free Heroku account. https://signup.heroku.com/

    Free Heroku account allows you to setup free dynos with
    550 run hours each month. If you verify your account 
    with a credit card, you'll receive 1000 free dyno hours 
    each month. This means you can run this example application
    24/7 for free on Heroku. A dyno is a worker, which
    executes application code.

2. Verify your Heroku account with a credit card
(optional, but recommended).

#### 3. Create a Discord Webhook
1. Perform the steps in the **'MAKING A WEBHOOK'** section of this article
https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks

2. Give your Webhook a name and a picture and choose the channel.

We will use the *Webhook URL* later in this guide.

_**DO NOT** perform the steps explained in the
'QUICK EXAMPLE: GITHUB WEBHOOK INTEGRATION' section!
Those steps are irrelevant for this example!_

#### 4. Setup Discord Developer Mode and Role IDs
1. Enable Discord Developer Mode.
    
    ![Developer Mode](../images/discord_advanced_mode.png)

2. Copy desired role ID(s).
    
    Find the role(s) you want to ping when the server
    goes unranked, right click and copy their IDs.
    
    ![Role ID](../images/discord_get_copy_role_id.png)    

3. Add role ID(s) to `ranked_alert.py`.

    ![Edit The File](../images/github_edit_unranked_alert.png)

    **Make sure you edit the file in the repository you just forked!**

    Open the file and look at lines 31 to 41.
    The role IDs are stored in the `PING_DISCORD_ROLES` variable.
    Read the comment lines starting with `#` for instructions.
    
4. In `ranked_alert.py` set `RUN = True`
on line number 8.

    ![Edits 1](../images/github_unranked_alert_run_true.png)

    ![Edits 2](../images/github_unranked_alert_changes.png)

5. Save (commit) the changes.

    ![Save Changes](../images/github_commit_unranked_alert_changes.png)

#### 5. Deploy on Heroku
1. Setup a new Heroku app & deploy from GitHub.

    - Go to https://dashboard.heroku.com/apps.
    - Click 'New' (top right corner).
    - Create new app.
    - Give your app a name & choose region.
    - Deployment method: GitHub
    
    ![Deploy](../images/heroku_deployment_method_github.png)

    - Enable automatic deploys.
    
    ![Automatic Deploys](../images/heroku_enable_automatic_deploys.png)

    - Connect to GitHub & choose your repository
    (the one you forked and edited).

2. Setup environment variables.

    - From the top bar, navigate to your app's settings.
    
    ![App Settings](../images/heroku_app_settings.png)
    
    - In settings, choose 'Reveal Config Vars'. Config Vars are your
    environment variables.
    
    ![Config Vars](../images/heroku_reveal_config_vars.png)
    
    - Setup your environment variables.
    - You have to setup `WEBADMIN_USERNAME_#`, `WEBADMIN_PASSWORD_#` and `WEBADMIN_URL_#`
    for each RS2 server you want to track.
    - The `#` starts from 1 and should be increased by 1 for every server you set up.
    - The example image has variables set up for 2 servers.
    - `DISCORD_WEBHOOK_URL_#` is the URL we created in [part 3](#3-create-a-discord-webhook) of this guide.
    - If you only have a single webhook URL, you can use the same webhook URL multiple times.
    - You may create new RS2 WebAdmin admin accounts for this bot, just make
    sure the accounts have access to the "Current Game" tab.
    
    ![Setup Config Vars](../images/heroku_setup_config_vars.png)

    - Finally, enable the dyno.
    
    ![Enable Dyno1](../images/heroku_enable_dyno_1.JPG)
    
    ![Enable Dyno1](../images/heroku_enable_dyno_2.JPG)

    - **If you can't see the enable dyno buttons, go to 'Deploy' tab,**
    **and at the end of the page, click 'Deploy Branch' (choose master branch)**.
    - Check your app logs.
    
    ![Heroku Logs](../images/heroku_view_logs.JPG)
    
    - If everything was set up correctly, you should have the following lines in your app log:
    ```
    2020-03-13T11:50:50.047845+00:00 app[worker.1]: running app: <module 'ranked_alert' from 'examples/unranked_discord_alert/ranked_alert.py'>
    2020-03-13T11:50:51.492858+00:00 app[worker.1]: 2 RS2WebAdmin instances initialized
    ```
   
#### 4. All done & extras!
There are also some extra features in `ranked_alert.py` that are commented
by prefixing with `#`, disabling them. You may uncomment these lines if you
wish to enable the extra features. Make sure the lines "line up" i.e. the
uncommented line is not intended by an extra whitespace.

E.g.
```python
# We could also change the map automatically.
# change_map(wa, "VNTE-Resort")
```
would be changed to:
```python
# We could also change the map automatically.
change_map(wa, "VNTE-Resort")
```
