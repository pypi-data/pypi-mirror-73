# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalpack',
 'royalpack.commands',
 'royalpack.events',
 'royalpack.stars',
 'royalpack.tables',
 'royalpack.types',
 'royalpack.utils']

package_data = \
{'': ['*'], 'royalpack': ['pycharm/*'], 'royalpack.commands': ['abstract/*']}

install_requires = \
['riotwatcher>=2.7.1,<3.0.0',
 'royalnet[telegram,discord,alchemy_easy,bard,constellation,sentry,herald,coloredlogs]>=5.10.3,<5.11.0',
 'royalspells>=3.2,<4.0',
 'steam']

setup_kwargs = {
    'name': 'royalpack',
    'version': '5.11.1',
    'description': 'A Royalnet command pack for the Royal Games community',
    'long_description': '# `royalpack`\n\n## Configuration\n\n```toml\n[Packs."royalpack"]\n\n# The main Telegram group\nTelegram.main_group_id = -1001153723135\n\n# The main Discord channel\nDiscord.main_channel_id = 566023556618518538\n\n# A Imgur API token (https://apidocs.imgur.com/?version=latest)\nImgur.token = "1234567890abcde"\n\n# A Steam Web API key (https://steamcommunity.com/dev/apikey)\nSteam.web_api_key = "123567890ABCDEF123567890ABCDEF12"\n\n# Should Royalnet automatically update the Dota ranks of all users?\nDota.updater.enabled = false\n\n# How many seconds should there be between two Dota updates?\nDota.updater.delay = 86400\n\n# Should Royalnet automatically update the League of Legends ranks of all users?\nLol.updater.enabled = false\n\n# How many seconds should there be between two League of Legends updates?\nLol.updater.delay = 86400\n\n# A League of Legends API token (https://developer.riotgames.com/)\nLol.token = "RGAPI-aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"\n\n# The region where your players are located\nLol.region = "euw1"\n\n# Should Royalnet automatically update the Brawlhalla ranks of all users?\nBrawlhalla.updater.enabled = false\n\n# How many seconds should there be between two League of Legends updates?\nBrawlhalla.updater.delay = 86400\n\n# A Brawlhalla API key (https://dev.brawlhalla.com/)\nBrawlhalla.api_key = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\n\n# The Peertube instance you want to use for new video notifications\nPeertube.instance_url = "https://pt.steffo.eu"\n\n# The delay in seconds between two new video checks\nPeertube.feed_update_timeout = 300\n\n# The Funkwhale instance you want to use for the fw commands\nFunkwhale.instance_url = "https://fw.steffo.eu"\n\n# The id of the role that users should have to be displayed by default in cv\nCv.displayed_role_id = 424549048561958912\n\n# The max duration of a song downloaded with the play commands\nPlay.max_song_duration = 7230\n\n# The Telegram channel where matchmaking messages should be sent in\nMatchmaking.mm_chat_id = -1001204402796\n\n```',
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalpack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
