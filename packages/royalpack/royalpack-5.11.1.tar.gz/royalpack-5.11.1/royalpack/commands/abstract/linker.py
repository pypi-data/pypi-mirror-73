from typing import *
import royalnet
import royalnet.commands as rc
import abc


class LinkerCommand(rc.Command, metaclass=abc.ABCMeta):

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        ...
