from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
import steam.steamid


class Steam:
    __tablename__ = "steam"

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def user(self):
        return relationship("User", backref=backref("steam"))

    @declared_attr
    def _steamid(self):
        return Column(BigInteger, primary_key=True)

    @property
    def steamid(self):
        return steam.steamid.SteamID(self._steamid)

    @declared_attr
    def persona_name(self):
        return Column(String)

    @declared_attr
    def profile_url(self):
        return Column(String)

    @declared_attr
    def avatar(self):
        return Column(String)

    @declared_attr
    def primary_clan_id(self):
        return Column(BigInteger)

    @declared_attr
    def account_creation_date(self):
        return Column(DateTime)

    def json(self):
        return {
            "steamid": self._steamid,
            "persona_name": self.persona_name,
            "profile_url": self.profile_url,
            "avatar": self.avatar,
            "primary_clan_id": self.primary_clan_id,
            "account_creation_date": self.account_creation_date.isoformat(),

            "dota": self.dota.json() if self.dota is not None else None,
            "brawlhalla": self.brawlhalla.json() if self.brawlhalla is not None else None
        }

    def __repr__(self):
        return f"<Steam account {self._steamid} of {self.user}>"

    def __str__(self):
        return f"[c]steam:{self._steamid}[/c]"
