from pyrogram import Client
from pytgcalls import GroupCallFactory

import config
from . import queues

client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
pytgcalls = GroupCallFactory(client)


@pytgcalls.on_stream_end()
def on_stream_end(chat_id: int) -> None:
    queues.task_done(chat_id)

    if queues.is_empty(chat_id):
        GroupCallFactory.leave_group_call(chat_id)
    else:
        GroupCallFactory.change_stream(
            chat_id, queues.get(chat_id)["file"]
        )


run = pytgcalls.run
