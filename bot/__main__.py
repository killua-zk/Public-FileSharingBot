#    This file is part of the FileSharing distribution.
#    Copyright (c) 2022 kaif-00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in
# <https://github.com/kaif-00z/Public-FileSharingBot/blob/main/License> .


from . import *
from .worker import *
from .database import get_info_own_iteam

bot.start(bot_token=Var.BOT_TOKEN)
LOGS.info("Bot starting...")


@bot.on(
    events.NewMessage(
        incoming=True, pattern="^/start ?(.*)", func=lambda e: e.is_private
    )
)
async def _(e):
    add_user(e.chat_id)
    if not (await is_joined(e.sender_id)):
        return # await e.reply("**Please Join @BotsBakery If You Want To Use This Bot**", buttons=[[Button.url("Bots Bakery", url="t.me/BotsBakery")]])
    u_id = e.pattern_match.group(1)
    if u_id:
        await get_iteams(e, u_id)
    else:
        await e.reply(
            f"Hi {e.sender.first_name}\n**I can store private files and others users can access files form shareable link**",
            buttons=[
                [Button.inline("HELP", data="help")],
                [
                    Button.url("SOURCE CODE", url="https://github.com/kaif-00z/"),
                    Button.url("DEVELOPER", url="t.me/kaif_00z"),
                ],
            ],
        )


@bot.on(events.NewMessage(incoming=True, pattern="^/create$", func=lambda e: e.is_private))
async def _(e):
    if not (await is_joined(e.sender_id)):
        return # await e.reply("**Please Join @BotsBakery If You Want To Use This Bot**", buttons=[[Button.url("Bots Bakery", url="t.me/BotsBakery")]])
    await gen_link(e)


@bot.on(events.NewMessage(incoming=True, pattern="^/revoke", func=lambda e: e.is_private))
async def _(e):
    if not (await is_joined(e.sender_id)):
        return # await e.reply("**Please Join @BotsBakery If You Want To Use This Bot**", buttons=[[Button.url("Bots Bakery", url="t.me/BotsBakery")]])
    try:
        link = e.text.split()[1]
    except:
        return await event.reply("`Link Not Given`")
    u_id = link.split("start=")[1]
    if u_id in get_info_own_iteam(e.sender_id):
        return await revoke_link(e, u_id)
    elif e.sender_id == Var.OWNER_ID:
        return await revoke_link(e, u_id)
    await e.reply("You Can't Revoke Someone else link")


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("help")))
async def _(e):
    await e.edit(
        "`/create` - __for generate link.__\n`/revoke <link>` - __for revoke the link.__\n`/list` __gives you list of links you created.__"
    )

@bot.on(events.NewMessage(incoming=True, pattern="^/list$", func=lambda e: e.is_private))
async def _(e):
    if not (await is_joined(e.sender_id)):
        return # await e.reply("**Please Join @BotsBakery If You Want To Use This Bot**", buttons=[[Button.url("Bots Bakery", url="t.me/BotsBakery")]])
    x = await e.reply("`Processing...`")
    loll = get_info_own_iteam(e.sender_id)
    txt = "**List Of Links**\n\n"
    try:
        for l in loll:
            txt +=  f"`•` https://t.me/{((await e.client.get_me()).username)}?start={l}\n"
        await x.edit(txt)
    except:
        await x.edit("`Something Went Wrong!`")


@bot.on(events.ChatAction)
async def _(e):
    await hmm(e)


@bot.on(events.NewMessage(incoming=True, pattern="\\/boardcast"))
async def _(e):
    await bcast(e)


LOGS.info("bot has started..")
bot.run_until_disconnected()
