=========
slack-cli
=========

**Modernized fork by Kirk Ford** - Bringing this awesome CLI tool into 2025! 🚀

This is a fully modernized version of the original `slack-cli <https://github.com/regisb/slack-cli>`_ by Régis Behmo. The original project was in maintenance mode, so I've updated it to work with current Slack API standards.

What's New in v3.0
==================

✨ **Fully compatible with 2025 Slack API standards:**

- Modern OAuth 2.0 authentication (bot & user tokens)
- Conversations API (replaces deprecated channels/groups/IM APIs)
- Socket Mode for real-time messaging
- Official ``slack_sdk`` library (replaced deprecated ``slacker``)
- Python 3.7+ support
- Bug fixes for DM messaging and username customization

**Upstream PR**: Contributing these changes back to the original project at `#45 <https://github.com/regisb/slack-cli/pull/45>`_

About slack-cli
===============

Interact with `Slack <https://slack.com/>`_ directly from your command line: send messages, upload files, pipe content, stream messages in real-time... all from the comfort of your terminal.

Perfect for automation, CI/CD pipelines, server monitoring, and productivity workflows.

.. image:: https://raw.githubusercontent.com/regisb/slack-cli/master/docs/demo.png

Quickstart
==========

::

    $ pip install git+https://github.com/KirkFord/slack-cli.git
    $ slack-cli -d general "Hello everyone!"


You will be asked to provide a Slack API token on first run. Check out the `Tokens`_ section below for setup instructions.

Migration from v2.x
===================

If you're upgrading from version 2.x, you'll need to:

1. **Python Version**: Upgrade to Python 3.7 or later
2. **Create a New Slack App**: Legacy tokens are no longer supported. Follow the instructions in the `Tokens`_ section to create a modern Slack App
3. **Update Your Token**: Delete your old token file and run slack-cli again to configure with your new bot token
4. **Socket Mode for Streaming**: If you use the ``-s`` flag for real-time streaming, you'll need an app-level token (see `Real-Time Streaming Setup`_ below)

The token configuration file location remains the same (``~/.config/slack-cli`` on Linux).

Usage
=====

::

    $ slack-cli -h
    usage: slack-cli [-h] [-t TOKEN] [-T TEAM] [-d DST] [-f FILE] [--pre] [--run]
                     [-u USER] [-s SRC] [-l LAST]
                     [messages [messages ...]]

    Send, pipe, upload and receive Slack messages from the CLI

    optional arguments:
      -h, --help            show this help message and exit
      -t TOKEN, --token TOKEN
                            Explicitly specify Slack API token which will be
                            saved to /home/user/.config/slack-cli/slack_token.
      -T TEAM, --team TEAM  Team domain to interact with. This is the name that
                            appears in the Slack url: https://xxx.slack.com. Use
                            this option to interact with different teams. If
                            unspecified, default to the team that was last used.

    Send messages:
      -d DST, --dst DST     Send message to a Slack channel, group or username
      -f FILE, --file FILE  Upload file
      --pre                 Send as verbatim `message`
      --run                 Run the message as a shell command and send both the
                            message and the command output
      -u USER, --user USER  Send message not as the current user, but as a bot
                            with the specified user name
      messages              Messages to send (messages can also be sent from
                            standard input)

    Receive messages:
      -s SRC, --src SRC     Receive messages from a Slack channel, group or
                            username. This option can be specified multiple times.
                            When streaming, use 'all' to stream from all sources.
      -l LAST, --last LAST  Print the last N messages. If this option is not
                            specified, messages will be streamed from the
                            requested sources.

Sending messages
----------------

The destination argument may be any user, group or channel::

    $ slack-cli -d general "Hello everyone!"
    $ slack-cli -d slackbot "Hello!"

Send message with a different username::

    $ slack-cli -d general -u terminator "I'll be back"

Update status
-------------

::

    $ slack-cli -d general "/status :office: In the office"
    $ slack-cli -d general "/status :house: At home"
    $ slack-cli -d general "/status Just chillin'"
    $ slack-cli -d general "/status clear"

Pipe content from stdin
~~~~~~~~~~~~~~~~~~~~~~~

::

    $ cat /etc/hosts | slack-cli -d devteam

Usually you will want to format piped content as verbatim content with triple backticks ("\`\`\`"). This is achieved with the ``--pre`` option::

    $ tail -f /var/log/nginx/access.log | slack-cli -d devteam --pre

Upload file
~~~~~~~~~~~

::

    $ slack-cli -f /etc/nginx/sites-available/default.conf -d alice

Run command and send output
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is really convenient for showing both the result of a command and the command itself::

    $ slack-cli -d john --run "git log -1"

will send to user ``john``::

    $ git log -1
    commit 013798f5c85043d31f0221a9a32b39298e97fb08
    Author: Régis Behmo <regis@behmo.com>
    Date:   Thu Jun 22 15:20:36 2017 +0200

        Replace all commands by a single command

        Our first 1.0 release!

Receiving messages
------------------

Stream to stdout
~~~~~~~~~~~~~~~~

Stream the content of a channel::

    $ slack-cli -s general

Monitor all conversations::

    $ slack-cli -s all

Dump (backup) the content of a channel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ slack-cli -s general --last 10000 > general.log
    $ slack-cli -s myboss --last 10000 > covermyass.log

Authentication
--------------

Switch to a different team
~~~~~~~~~~~~~~~~~~~~~~~~~~

Switch to a different team anytime with the ``-T`` flag::

    $ slack-cli -T family -d general "I'll be home in an hour"

The new team will become the new default team.

Token management
~~~~~~~~~~~~~~~~

Note that the Slack token may optionally be stored in an environment variable (although it is not recommended `for security reasons <https://unix.stackexchange.com/questions/369566/why-is-passing-the-secrets-via-environmental-variables-considered-extremely-ins>`_)::

    $ export SLACK_TOKEN="slack_token_string"

The ``slack-cli`` configuration is stored in a generic configuration directory -- by default, this is ~/.config/slack-cli on Linux. You can check the path of this directory by running::

    python3 -c "from slackcli.token import CONFIG_ROOT; print(CONFIG_ROOT)"

This directory can be modified by setting the ``SLACK_CLI_CONFIG_ROOT`` environment variable. For instance::

    export SLACK_CLI_CONFIG_ROOT=~/slackcli

Bells and Whistles ᕕ(⌐■_■)ᕗ ♪♬
------------------------------

Autocomplete
~~~~~~~~~~~~

Channel, group and user names can be autocompleted from the command line for `bash` users. Add the following line to `~/.bashrc`::

    eval "$(register-python-argcomplete slack-cli)"

Then, try autocompletion with::

    $ slack -s gene<tab>

or::

    $ slack -d <tab><tab>

Unfortunately, I did not manage to get autocompletion to work with ``zsh`` ¯\\_( ͡° ͜ʖ ͡°)_/¯ Please let me know if you have more success.

Colors
~~~~~~

Color output is activated by default in compatible terminals. To deactivate colors, define the ``SLACK_CLI_NO_COLOR`` environment variable::

    export SLACK_CLI_NO_COLORS=1

Emojis
~~~~~~

Emoji short codes will be automatically replaced by their corresponding unicode value. For instance, ``:smile:`` will become 😄. However, **these characters will display properly only if your terminal supports them!** I stronly encourage you to download patched fonts from `Nerd Fonts <https://nerdfonts.com/>`_ and to configure your terminal to use them. For instance, in Ubuntu this is how I downloaded the DejaVuSansMono fonts::

    wget -O ~/.fonts/DejaVuSansMono.zip https://github.com/ryanoasis/nerd-fonts/releases/download/v2.0.0/DejaVuSansMono.zip
    cd ~/.fonts
    unzip DejaVuSansMono.zip
    fc-cache -vf ~/.fonts

If emojis are not your thing, you can disable them globally with the ``SLACK_CLI_NO_EMOJI`` environment variable::

    export SLACK_CLI_NO_EMOJI=1

Tokens
~~~~~~

To generate a bot token for slack-cli:

1. Create a `new Slack App <https://api.slack.com/apps/new>`__ and add it to your workspace
2. Under **OAuth & Permissions**, add the following Bot Token Scopes:

   Required scopes for basic functionality:

   - ``channels:read`` - List public channels
   - ``groups:read`` - List private channels
   - ``im:read`` - List direct messages
   - ``users:read`` - List users
   - ``chat:write`` - Send messages

   Additional scopes for full functionality:

   - ``channels:history`` - Read message history from public channels
   - ``groups:history`` - Read message history from private channels
   - ``im:history`` - Read message history from DMs
   - ``files:write`` - Upload files
   - ``team:read`` - Get team info (optional, for multi-team support)

3. Click **Install to Workspace** and authorize your app
4. Copy the **Bot User OAuth Token** (starts with ``xoxb-``)
5. Run slack-cli and paste the token when prompted

.. figure:: https://raw.githubusercontent.com/regisb/slack-cli/master/docs/token.png
   :alt: OAuth Access Token

Real-Time Streaming Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use real-time message streaming (``slack-cli -s general``), you need to:

1. In your Slack App settings, go to **Socket Mode** and enable it
2. Under **Basic Information** > **App-Level Tokens**, click **Generate Token and Scopes**
3. Name it (e.g., "socket-mode") and add the ``connections:write`` scope
4. Generate and copy the app-level token (starts with ``xapp-``)
5. Subscribe to the ``message.channels`` event under **Event Subscriptions**
6. Run ``slack-cli -s general`` and paste the app-level token when prompted

The app-level token will be saved separately and only used for streaming.


Development
-----------

About This Fork
~~~~~~~~~~~~~~~

This is Kirk Ford's modernized fork of the original `slack-cli <https://github.com/regisb/slack-cli>`_ project. All v3.0 modernization work was completed in collaboration with Claude Code to bring this tool up to 2025 standards.

**Original Author**: Régis Behmo (`@regisb <https://github.com/regisb>`_)

**Modernization**: Kirk Ford (`@KirkFord <https://github.com/KirkFord>`_)

**Upstream PR**: `#45 <https://github.com/regisb/slack-cli/pull/45>`_ - Contributing these improvements back to the original project

Contributions
~~~~~~~~~~~~~

Found a bug or have a feature request? Please `open an issue <https://github.com/KirkFord/slack-cli/issues>`_ or submit a pull request!

This work is licensed under the terms of the `MIT License <https://tldrlegal.com/license/mit-license>`_

Project History
~~~~~~~~~~~~~~~

- **Original Project**: `slacker-cli <https://github.com/juanpabloaj/slacker-cli/>`_ by Juan Pablo Arenas
- **slack-cli v1-v2**: Régis Behmo's complete rewrite and evolution
- **slack-cli v3.0**: Kirk Ford's modernization for 2025 Slack API standards

Tests
~~~~~

Install the development requirements::
    
    pip install -e .[development]

Run all tests::
    
    make test

Format your code with `black <https://black.readthedocs.io/en/stable/>`__::

    make format

Update emojis
~~~~~~~~~~~~~

::

    python -c "from slackcli.emoji import Emojis; Emojis.download()"
