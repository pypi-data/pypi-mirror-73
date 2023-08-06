from typing import *
import steam.steamid
import steam.webapi
import datetime
import royalnet.commands as rc
import royalnet.utils as ru

from ..tables import Steam, FiorygiTransaction


class SteampoweredCommand(rc.Command):
    name: str = "steampowered"

    description: str = "Connetti il tuo account di Steam!"

    syntax: str = "{profile_url}"

    def __init__(self, interface: rc.CommandInterface):
        super().__init__(interface)
        if "Steam" not in self.config or "web_api_key" not in self.config["Steam"]:
            raise rc.ConfigurationError("[c]Steam.web_api_key[/c] config option is missing!")
        self._api = steam.webapi.WebAPI(self.config["Steam"]["web_api_key"])

    @staticmethod
    def _display(account: Steam):
        string = f"ℹ️ [url={account.profile_url}]{account.persona_name}[/url]\n" \
                 f"[b]Level {account.account_level}[/b]\n" \
                 f"\n" \
                 f"Owned games: [b]{account.owned_games_count}[/b]\n" \
                 f"Most played 2 weeks: [url=https://store.steampowered.com/app/{account.most_played_game_2weeks}]{account.most_played_game_2weeks}[/url]\n" \
                 f"Most played forever: [url=https://store.steampowered.com/app/{account.most_played_game_forever}]{account.most_played_game_forever}[/url]\n" \
                 f"\n" \
                 f"SteamID: [c]{account.steamid.as_32}[/c]\n" \
                 f"SteamID2: [c]{account.steamid.as_steam2}[/c]\n" \
                 f"SteamID3: [c]{account.steamid.as_steam3}[/c]\n" \
                 f"SteamID64: [c]{account.steamid.as_64}[/c]\n" \
                 f"\n" \
                 f"Created on: [b]{account.account_creation_date}[/b]\n"
        return string

    async def _call(self, method, *args, **kwargs):
        try:
            return await ru.asyncify(method, *args, **kwargs)
        except Exception as e:
            raise rc.ExternalError("\n".join(e.args).replace(self.config["Steam"]["web_api_key"], "HIDDEN"))

    async def _update(self, account: Steam):
        # noinspection PyProtectedMember
        response = await self._call(self._api.ISteamUser.GetPlayerSummaries_v2, steamids=account._steamid)
        r = response["response"]["players"][0]
        account.persona_name = r["personaname"]
        account.profile_url = r["profileurl"]
        account.avatar = r["avatar"]
        account.primary_clan_id = r["primaryclanid"]
        account.account_creation_date = datetime.datetime.fromtimestamp(r["timecreated"])

        # noinspection PyProtectedMember
        response = await self._call(self._api.IPlayerService.GetSteamLevel_v1, steamid=account._steamid)
        account.account_level = response["response"]["player_level"]

        # noinspection PyProtectedMember
        response = await self._call(self._api.IPlayerService.GetOwnedGames_v1,
                                    steamid=account._steamid,
                                    include_appinfo=False,
                                    include_played_free_games=True,
                                    include_free_sub=False,
                                    appids_filter=None)
        account.owned_games_count = response["response"]["game_count"]
        if response["response"]["game_count"] >= 0:
            account.most_played_game_2weeks = sorted(response["response"]["games"], key=lambda g: -g.get("playtime_2weeks", 0))[0]["appid"]
            account.most_played_game_forever = sorted(response["response"]["games"], key=lambda g: -g.get("playtime_forever", 0))[0]["appid"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        author = await data.get_author()
        if len(args) > 0:
            url = args.joined()
            steamid64 = await self._call(steam.steamid.steam64_from_url, url)
            if steamid64 is None:
                raise rc.InvalidInputError("Quel link non è associato ad alcun account Steam.")
            response = await self._call(self._api.ISteamUser.GetPlayerSummaries_v2, steamids=steamid64)
            r = response["response"]["players"][0]
            steam_account = self.alchemy.get(Steam)(
                user=author,
                _steamid=int(steamid64),
                persona_name=r["personaname"],
                profile_url=r["profileurl"],
                avatar=r["avatarfull"],
                primary_clan_id=r["primaryclanid"],
                account_creation_date=datetime.datetime.fromtimestamp(r["timecreated"])
            )
            data.session.add(steam_account)
            await data.session_commit()
            await data.reply(f"↔️ Account {steam_account} connesso a {author}!")
            await FiorygiTransaction.spawn_fiorygi(data, author, 1,
                                                   "aver connesso il proprio account di Steam a Royalnet")
        else:
            # Update and display the Steam info for the current account
            if len(author.steam) == 0:
                raise rc.UserError("Nessun account di Steam trovato.")
            message = ""
            for account in author.steam:
                await self._update(account)
                message += self._display(account)
                message += "\n"
            await data.session_commit()
            await data.reply(message)
