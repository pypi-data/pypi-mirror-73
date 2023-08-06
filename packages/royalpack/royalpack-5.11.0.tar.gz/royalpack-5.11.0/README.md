# `royalpack`

## Configuration

```toml
[Packs."royalpack"]

# The main Telegram group
Telegram.main_group_id = -1001153723135

# The main Discord channel
Discord.main_channel_id = 566023556618518538

# A Imgur API token (https://apidocs.imgur.com/?version=latest)
Imgur.token = "1234567890abcde"

# A Steam Web API key (https://steamcommunity.com/dev/apikey)
Steam.web_api_key = "123567890ABCDEF123567890ABCDEF12"

# Should Royalnet automatically update the Dota ranks of all users?
Dota.updater.enabled = false

# How many seconds should there be between two Dota updates?
Dota.updater.delay = 86400

# Should Royalnet automatically update the League of Legends ranks of all users?
Lol.updater.enabled = false

# How many seconds should there be between two League of Legends updates?
Lol.updater.delay = 86400

# A League of Legends API token (https://developer.riotgames.com/)
Lol.token = "RGAPI-aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

# The region where your players are located
Lol.region = "euw1"

# Should Royalnet automatically update the Brawlhalla ranks of all users?
Brawlhalla.updater.enabled = false

# How many seconds should there be between two League of Legends updates?
Brawlhalla.updater.delay = 86400

# A Brawlhalla API key (https://dev.brawlhalla.com/)
Brawlhalla.api_key = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

# The Peertube instance you want to use for new video notifications
Peertube.instance_url = "https://pt.steffo.eu"

# The delay in seconds between two new video checks
Peertube.feed_update_timeout = 300

# The Funkwhale instance you want to use for the fw commands
Funkwhale.instance_url = "https://fw.steffo.eu"

# The id of the role that users should have to be displayed by default in cv
Cv.displayed_role_id = 424549048561958912

# The max duration of a song downloaded with the play commands
Play.max_song_duration = 7230

# The Telegram channel where matchmaking messages should be sent in
Matchmaking.mm_chat_id = -1001204402796

```