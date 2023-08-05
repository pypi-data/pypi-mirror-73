import contextlib
from typing import *
import datetime
import re
import dateparser
import typing
import random
import enum
import asyncio as aio
from telegram import Message as PTBMessage
from telegram import InlineKeyboardMarkup as InKM
from telegram import InlineKeyboardButton as InKB
from telegram.error import TelegramError
import royalnet.commands as rc
from royalnet.serf.telegram import escape as telegram_escape
from royalnet.utils import asyncify, sleep_until, sentry_async_wrap
import logging

from ..tables import MMEvent, MMResponse, FiorygiTransaction
from ..types import MMChoice, MMInterfaceDataTelegram


class Interrupts(enum.Enum):
    TIME_RAN_OUT = enum.auto()
    MANUAL_START = enum.auto()
    MANUAL_DELETE = enum.auto()


mmchoice_sorting = {
    MMChoice.YES: -4,
    MMChoice.LATE_SHORT: -3,
    MMChoice.LATE_MEDIUM: -2,
    MMChoice.LATE_LONG: -1,
    MMChoice.MAYBE: 0,
    MMChoice.NO: 1
}


class MMTask:
    def __init__(self, mmid: int, *, command: rc.Command):
        log.debug(f"Creating task for: {mmid}")

        self.loop: aio.AbstractEventLoop = command.loop
        self.task: Optional[aio.Task] = None
        self.queue: aio.Queue = aio.Queue(loop=self.loop)
        self.command: rc.Command = command
        self.mmid: int = mmid

        self._session: Optional = None
        self._EventT: Optional[Type[MMEvent]] = None
        self._ResponseT: Optional[Type[MMResponse]] = None
        self._mmevent: Optional[MMEvent] = None

    @property
    def is_running(self):
        return self.task is not None

    def get_response_line(self, response: MMResponse):
        # noinspection PyListCreation
        line = []

        # Emoji
        line.append(f"{response.choice.value}")

        # Mention the user if he said yes, otherwise just display his name
        if response.choice == MMChoice.NO:
            line.append(f"{response.user.telegram[0].name()}")
        else:
            line.append(f"{response.user.telegram[0].mention()}")

        # Late time
        if response.choice == MMChoice.LATE_SHORT:
            td = self._mmevent.datetime + datetime.timedelta(minutes=10)
            line.append(f"[{td.strftime('%H:%M')}]")

        elif response.choice == MMChoice.LATE_MEDIUM:
            td = self._mmevent.datetime + datetime.timedelta(minutes=30)
            line.append(f"[{td.strftime('%H:%M')}]")

        elif response.choice == MMChoice.LATE_LONG:
            td = self._mmevent.datetime + datetime.timedelta(minutes=60)
            line.append(f"[{td.strftime('%H:%M')}+]")

        # Creator
        if response.user == self._mmevent.creator:
            line.append("👑")

        # Result
        return " ".join(line)

    @property
    def channel_text(self) -> str:
        # noinspection PyListCreation
        text = []

        # First line
        if self._mmevent.datetime is None:
            text.append(f"🌐 [Prossimamente] [b]{self._mmevent.title}[/b]")
        else:
            text.append(f"🚩 [{self._mmevent.datetime.strftime('%Y-%m-%d %H:%M')}] [b]{self._mmevent.title}[/b]")

        # Description
        if self._mmevent.description:
            text.append(f"{self._mmevent.description}")

        # Spacer
        text.append("")

        # Responses
        responses = sorted(self._mmevent.responses, key=lambda r: mmchoice_sorting[r.choice])
        for response in responses:
            text.append(self.get_response_line(response))

        # Result
        return "\n".join(text)

    @property
    def start_text(self) -> str:
        # noinspection PyListCreation
        text = []

        # First line
        if self._mmevent.datetime is None:
            text.append(f"🌐 Le iscrizioni all'evento [b]{self._mmevent.title}[/b] sono terminate!")
        else:
            text.append(f"🚩 L'evento [b]{self._mmevent.title}[/b] è iniziato!")

        # Description
        if self._mmevent.description:
            text.append(f"{self._mmevent.description}")

        # Spacer
        text.append("")

        # Responses
        responses = sorted(self._mmevent.responses, key=lambda r: mmchoice_sorting[r.choice])
        for response in responses:
            text.append(self.get_response_line(response))

        # Result
        return "\n".join(text)

    @property
    def delete_text(self) -> str:
        return f"🗑 L'evento [b]{self._mmevent.title}[/b] è stato eliminato."

    def get_answer_callback(self, choice: MMChoice):
        async def callback(data: rc.CommandData):
            # Find the user who clicked on the button
            user = await data.get_author(error_if_none=True)

            # Get the related MMEvent
            mmevent: MMEvent = await asyncify(data.session.query(self._EventT).get, self.mmid)

            # Check if the user had already responded
            mmresponse: MMResponse = await asyncify(
                data.session.query(self._ResponseT).filter_by(user=user, mmevent=mmevent).one_or_none
            )

            if mmresponse is None:
                # If they didn't respond, create a new MMResponse
                mmresponse = self._ResponseT(user=user, mmevent=mmevent, choice=choice)
                data.session.add(mmresponse)

                # Drop fiorygi
                if random.randrange(100) < self.command.config["Matchmaking"]["fiorygi_award_chance"]:
                    await FiorygiTransaction.spawn_fiorygi(data, user, 1, "aver risposto a un matchmaking")
            else:
                # Change their response
                mmresponse.choice = choice
            await data.session_commit()

            await self.telegram_channel_message_update()

            await data.reply(f"{choice.value} Hai risposto al matchmaking!")
        return callback

    def get_delete_callback(self):
        async def callback(data: rc.CommandData):
            # Find the user who clicked on the button
            user = await data.get_author(error_if_none=True)

            # Get the related MMEvent
            mmevent: MMEvent = await asyncify(data.session.query(self._EventT).get, self.mmid)

            # Ensure the user has the required roles to start the matchmaking
            if user != mmevent.creator and "admin" not in user.roles:
                raise rc.UserError("Non hai i permessi per eliminare questo matchmaking!")

            # Interrupt the matchmaking with the MANUAL_DELETE reason
            await self.queue.put(Interrupts.MANUAL_DELETE)

            await data.reply(f"🗑 Evento eliminato!")
        return callback

    def get_start_callback(self):
        async def callback(data: rc.CommandData):
            # Find the user who clicked on the button
            user = await data.get_author(error_if_none=True)

            # Get the related MMEvent
            mmevent: MMEvent = await asyncify(data.session.query(self._EventT).get, self.mmid)

            # Ensure the user has the required roles to start the matchmaking
            if user != mmevent.creator and "admin" not in user.roles:
                raise rc.UserError("Non hai i permessi per eliminare questo matchmaking!")

            # Interrupt the matchmaking with the MANUAL_DELETE reason
            await self.queue.put(Interrupts.MANUAL_START)

            await data.reply(f"🚩 Evento avviato!")
        return callback

    @property
    def royalnet_keyboard(self):
        # noinspection PyListCreation
        rows = []

        rows.append([
            rc.KeyboardKey(
                interface=self.command.interface,
                short=f"{MMChoice.YES.value}",
                text="Ci sarò!",
                callback=self.get_answer_callback(MMChoice.YES)
            ),
            rc.KeyboardKey(
                interface=self.command.interface,
                short=f"{MMChoice.MAYBE.value}",
                text="Forse...",
                callback=self.get_answer_callback(MMChoice.MAYBE)
            ),
            rc.KeyboardKey(
                interface=self.command.interface,
                short=f"{MMChoice.NO.value}",
                text="Non mi interessa.",
                callback=self.get_answer_callback(MMChoice.NO)
            ),
        ])

        if self._mmevent.datetime is not None:
            rows.append([
                rc.KeyboardKey(
                    interface=self.command.interface,
                    short=f"{MMChoice.LATE_SHORT.value}",
                    text="10 min",
                    callback=self.get_answer_callback(MMChoice.LATE_SHORT)
                ),
                rc.KeyboardKey(
                    interface=self.command.interface,
                    short=f"{MMChoice.LATE_MEDIUM.value}",
                    text="30 min",
                    callback=self.get_answer_callback(MMChoice.LATE_MEDIUM)
                ),
                rc.KeyboardKey(
                    interface=self.command.interface,
                    short=f"{MMChoice.LATE_LONG.value}",
                    text="60 min",
                    callback=self.get_answer_callback(MMChoice.LATE_LONG)
                )
            ])

        rows.append([
            rc.KeyboardKey(
                interface=self.command.interface,
                short=f"🗑",
                text="Elimina",
                callback=self.get_delete_callback()
            ),
            rc.KeyboardKey(
                interface=self.command.interface,
                short=f"🚩",
                text="Inizia",
                callback=self.get_start_callback()
            ),
        ])

        return rows

    @property
    def telegram_keyboard(self):
        # noinspection PyListCreation
        rows = []
        key_id = 0

        for r_row in self.royalnet_keyboard:
            row = []
            for r_key in r_row:
                # Generate a unique callback string
                callback_str = f"mm{self.mmid}_{key_id}"

                # Create a InlineKeyboardButton with that callback string
                row.append(InKB(f"{r_key.short} {r_key.text}", callback_data=callback_str))

                # Increase the key_id
                key_id += 1
            rows.append(row)

        # Return the resulting InlineKeyboardMarkup
        return InKM(rows)

    def register_telegram_keyboard(self, inkm: InKM):
        # noinspection PyListCreation
        royalnet_keyboard = self.royalnet_keyboard
        for x, row in enumerate(inkm.inline_keyboard):
            for y, key in enumerate(row):
                key: InKB
                self.command.interface.serf.register_keyboard_key(key.callback_data, key=royalnet_keyboard[x][y])

    def unregister_telegram_keyboard(self, inkm: InKM):
        for row in inkm.inline_keyboard:
            for key in row:
                key: InKB
                self.command.interface.serf.unregister_keyboard_key(key.callback_data)

    async def wait_until_due(self):
        """When the event is due, interrupt the MMTask with the TIME_RAN_OUT reason."""
        if self._mmevent.datetime is None:
            return
        await sleep_until(self._mmevent.datetime)
        await self.queue.put(Interrupts.TIME_RAN_OUT)

    @property
    def telegram_channel_id(self):
        return self.command.config["Matchmaking"]["mm_telegram_channel_id"]

    @property
    def telegram_group_id(self):
        return self.command.config["Matchmaking"]["mm_telegram_group_id"]

    @contextlib.asynccontextmanager
    async def telegram_channel_message(self):

        # Generate the InlineKeyboardMarkup
        inkm = self.telegram_keyboard

        # Bind the Royalnet buttons to the Telegram keyboard
        log.debug(f"Registering keyboard for: {self.mmid}")
        self.register_telegram_keyboard(inkm)

        # If the event has no associated interface data...
        if self._mmevent.interface_data is None:
            # Send the channel message
            log.debug(f"Sending message for: {self.mmid}")
            message: PTBMessage = await self.command.interface.serf.api_call(
                self.command.interface.serf.client.send_message,
                chat_id=self.telegram_channel_id,
                text=telegram_escape(self.channel_text),
                parse_mode="HTML",
                disable_webpage_preview=True,
                reply_markup=inkm
            )

            # Register the interface data on the database
            self._mmevent.interface_data = MMInterfaceDataTelegram(
                chat_id=self.telegram_channel_id,
                message_id=message.message_id
            )
            self._session.commit()

        # Wait until the event starts
        yield

        # Delete the channel message
        log.debug(f"Deleting message for: {self.mmid}")
        await self.command.interface.serf.api_call(
            self.command.interface.serf.client.delete_message,
            chat_id=self._mmevent.interface_data.chat_id,
            message_id=self._mmevent.interface_data.message_id
        )

        # Unregister the Telegram keyboard bindings
        log.debug(f"Unregistering keyboard for: {self.mmid}")
        self.unregister_telegram_keyboard(inkm)

    async def telegram_channel_message_update(self):
        try:
            await self.command.interface.serf.api_call(
                self.command.interface.serf.client.edit_message_text,
                chat_id=self._mmevent.interface_data.chat_id,
                text=telegram_escape(self.channel_text),
                message_id=self._mmevent.interface_data.message_id,
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup=self.telegram_keyboard
            )
        except TelegramError as e:
            log.warning(f"TelegramError during update: {e}")

    async def telegram_group_message_start(self):
        await self.command.interface.serf.api_call(
            self.command.interface.serf.client.send_message,
            chat_id=self.telegram_group_id,
            text=telegram_escape(self.start_text),
            parse_mode="HTML",
            disable_webpage_preview=True
        )

    async def telegram_group_message_delete(self):
        await self.command.interface.serf.api_call(
            self.command.interface.serf.client.send_message,
            chat_id=self.telegram_group_id,
            text=telegram_escape(self.delete_text),
            parse_mode="HTML",
            disable_webpage_preview=True
        )

    def start(self):
        log.debug(f"Starting task for: {self.mmid}")
        self.task = self.loop.create_task(self.run())

    @sentry_async_wrap()
    async def run(self):
        log.debug(f"Running task for: {self.mmid}")

        # Create a new session for the MMTask
        self._session = self.command.alchemy.Session()
        self._EventT = self.command.alchemy.get(MMEvent)
        self._ResponseT = self.command.alchemy.get(MMResponse)
        self._mmevent: MMEvent = self._session.query(self._EventT).get(self.mmid)

        if self._mmevent is None:
            raise rc.InvalidInputError(f"No event exists with the mmid {self.mmid}.")

        if self._mmevent.interface != "telegram":
            raise rc.UnsupportedError("Currently only the Telegram interface is supported.")

        async with self.telegram_channel_message():
            self.loop.create_task(self.wait_until_due())

            # Sleep until something interrupts the task
            interrupt = await self.queue.get()

            # Mark the event as interrupted
            self._mmevent.interrupted = True
            await self._session.commit()

        # Send a group notification if the MMEvent wasn't deleted
        if interrupt != Interrupts.MANUAL_DELETE:
            await self.telegram_group_message_start()
        else:
            await self.telegram_group_message_delete()

        # Close the database session
        await asyncify(self._session.close)


log = logging.getLogger(__name__)


class MatchmakingCommand(rc.Command):
    name: str = "matchmaking"

    description: str = "Cerca persone per una partita a qualcosa!"

    syntax: str = ""

    aliases = ["mm", "lfg"]

    def __init__(self, interface: rc.CommandInterface):
        super().__init__(interface)

        # Find all active MMEvents and run the tasks for them
        session = self.alchemy.Session()

        # Create a new MMEvent and run it
        if self.interface.name == "telegram":
            MMEventT = self.alchemy.get(MMEvent)
            active_mmevents = (
                session
                .query(MMEventT)
                .filter(
                    MMEventT.interface == self.interface.name,
                    MMEventT.interrupted == False
                )
                .all()
            )
            for mmevent in active_mmevents:
                task = MMTask(mmevent.mmid, command=self)
                task.start()

    @staticmethod
    def _parse_args(args) -> Tuple[Optional[datetime.datetime], str, str]:
        """Parse command arguments, either using the standard syntax or the Proto syntax."""
        try:
            timestring, title, description = args.match(r"(?:\[\s*([^]]+)\s*]\s*)?([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        except rc.InvalidInputError:
            timestring, title, description = args.match(r"(?:\s*(.+?)\s*\n\s*)?([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        if timestring is not None:
            try:
                dt: typing.Optional[datetime.datetime] = dateparser.parse(timestring, settings={
                    "PREFER_DATES_FROM": "future"
                })
            except OverflowError:
                dt = None
            if dt is None:
                raise rc.InvalidInputError("La data che hai specificato non è valida.")
            if dt <= datetime.datetime.now():
                raise rc.InvalidInputError("La data che hai specificato è nel passato.")
            if dt - datetime.datetime.now() >= datetime.timedelta(days=366):
                raise rc.InvalidInputError("Hai specificato una data tra più di un anno!\n"
                                           "Se volevi scrivere un'orario, ricordati che le ore sono separate da "
                                           "due punti (:) e non da punto semplice!")
        else:
            dt = None
        return dt, title, description

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        """Handle a matchmaking command call."""
        author = await data.get_author(error_if_none=True)

        # Parse the arguments, either with the standard syntax or with the Proto syntax
        dt, title, description = self._parse_args(args)

        # Add the MMEvent to the database
        mmevent: MMEvent = self.alchemy.get(MMEvent)(creator=author,
                                                     datetime=dt,
                                                     title=title,
                                                     description=description,
                                                     interface=self.interface.name)
        data.session.add(mmevent)
        await data.session_commit()

        # Create and run a task for the newly created MMEvent
        task = MMTask(mmevent.mmid, command=self)
        task.start()

        await data.reply(f"🚩 Matchmaking creato!")
