# Changelog

## v3.0.0 (2025-01-06) - Major Modernization Update

**🎉 Fully modernized for 2025 Slack API standards!**

### Breaking Changes

- **Python 3.7+ Required**: Dropped support for Python 2 and Python 3.3-3.6
- **Legacy Tokens No Longer Supported**: Must create a modern Slack App with OAuth 2.0
  - Bot tokens (`xoxb-`) are now required instead of legacy tokens
  - Legacy token URL removed from prompts
- **Socket Mode for Streaming**: Real-time message streaming (`-s` flag) now requires an app-level token (`xapp-`)
  - Old RTM API replaced with modern Socket Mode
  - Users must enable Socket Mode in their Slack App settings

### Migration Guide

For users upgrading from v2.x:

1. Upgrade to Python 3.7 or later
2. Create a new Slack App at https://api.slack.com/apps/new
3. Add required OAuth scopes (see README for full list):
   - `channels:read`, `groups:read`, `im:read`, `users:read`
   - `chat:write`, `channels:history`, `groups:history`, `im:history`
   - `files:write` (for file uploads)
4. Install app to workspace and copy Bot User OAuth Token
5. Delete old token file: `rm ~/.config/slack-cli/slack_token`
6. Run slack-cli and enter your new bot token
7. For streaming: Enable Socket Mode and create app-level token with `connections:write` scope

### New Features & Improvements

- **Modern Slack SDK**: Migrated from deprecated `slacker` library to official `slack_sdk` (v3.37.0+)
- **Conversations API**: All API calls now use the modern, unified Conversations API
  - `conversations.list` replaces deprecated `channels.list`, `groups.list`, `im.list`
  - `conversations.history` replaces separate history methods
  - `conversations.info` provides unified channel/group information
- **Updated File Upload**: Migrated to `files_upload_v2` (old method deprecated May 2025)
- **Socket Mode**: Modern WebSocket-based real-time messaging
- **Better Error Handling**: Improved error messages with `SlackApiError`
- **Updated Documentation**: Comprehensive migration guide and setup instructions

### Technical Changes

- Replaced `slacker.Slacker` with `slack_sdk.WebClient`
- Updated all API method calls to use snake_case (e.g., `users_info`, `chat_postMessage`)
- API responses now return dicts directly (no `.body` attribute)
- Added app-level token storage for Socket Mode
- Removed `websocket-client` dependency (handled by slack_sdk)

### Deprecation Notices

The following APIs used in v2.x are now fully replaced:

- ❌ `rtm.start()` → ✅ Socket Mode with Events API
- ❌ `channels.list()` → ✅ `conversations.list(types="public_channel")`
- ❌ `groups.list()` → ✅ `conversations.list(types="private_channel")`
- ❌ `im.list()` → ✅ `conversations.list(types="im")`
- ❌ `files.upload()` → ✅ `files_upload_v2()`

---

## v2.2.7 (2020-05-11)

- Support `/status clear` and extended status updates.
- Make it possible to run slack-cli without a writable configuration directory

## v2.2.6 (2020-01-22)

- Support status updates

## v2.2.4 (2019-02-17)

- Fix crash on receiving private group message

## v2.2.3 (2019-01-16)

- Properly identify bots
- Properly print bot messages

## v2.2.1 (2018-12-22)

- Colorized output
- Emojis!

## v2.1.2 (2018-12-21)

- CLI bash autocompletion
- Fix default token saving on team change

## v2.1.1 (2018-12-20)

- Correctly print user and channel names

## v2.1.0 (2018-12-07)

- Faster search/stream
- Stream from all channels (``-s all``)
- Send messages as a different user (``-u terminator``)

## v2.0.2 (2017-09-13)

- Better error management

## v2.0.1 (2017-09-09)

- Simplify reading from stdin

## v2.0.0 (2017-09-09)

- Add support for multiple teams
- Fix streaming issues
- Improve printed message format
- Simplify sending messages from stdin

## v1.0.3 (2017-09-04):

- Add "--last" flag to print an entire conversation

## v1.0.2 (2017-08-31):

- Fix token verification issue for users that don't have a "general" channel

## v1.0 (2017-07-06):

- Refactor command line by reducing all commands to a single "slack-cli" command.
- Interactive API token input.
- Automatic token creation check.
    
