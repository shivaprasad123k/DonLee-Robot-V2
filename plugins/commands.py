# (c) @SpEcHIDe
# (c) @AlbertEinsteinTG
# (c) @Muhammed_RK, @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee_Robot/blob/main/LICENSE

import logging

import re, random, asyncio, aiofiles, aiofiles.os, datetime, traceback, random, string, time, os
from random import choice
logger = logging.getLogger(__name__)
from pyrogram import Client
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from translation import Translation
from donlee_robot.logger import LOGGER, VERIFY
from database import Database, send_msg
from donlee_robot.donlee_robot import DonLee_Robot
from config import PHOTO, OWNER_ID, FORCE_CHANNEL, CUSTOM_CAPTION, DEV_USERNAME, DEV_NAME, FORCE_SUB_TEXT, GROUP, GROUP_LINK, CHANNEL, CHANNEL_LINK, BOLD
from pyrogram.errors import UserNotParticipant, FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from translation import Translation 

db = Database()
broadcast_ids = {}
HAAAAAAAAA = f"t.me/{GROUP_LINK}"
# # # @DonLee_Robot # # #

update_channel = FORCE_CHANNEL
@DonLee_Robot.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
    try:
        file_uid = message.command[1]
    except IndexError:
        file_uid = False
             
    if file_uid:
        try:
            user = await bot.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked out":
               await message.reply_text("😔 Sorry Dude, You are **🅱︎🅰︎🅽︎🅽︎🅴︎🅳︎ 🤣🤣🤣**")
               return
        except UserNotParticipant:
            userbot = await bot.get_me()
            await message.reply_text(
                text=FORCE_SUB_TEXT.format(message.from_user.mention),
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="🔔 Join", url=f"https://t.me/{update_channel}")]       
              ])
            )
            return
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return

        if BOLD == "bold":
            caption = ("<b>" + file_name + "</b>")
        else:
            caption = ("<code>" + file_name + "</code>")
        try:
            await message.reply_cached_media(
                file_id,
                quote=True,
                caption = f"""{caption}\n\n{CUSTOM_CAPTION}""",
                parse_mode="html",
                reply_markup=db.Donlee_bt
            )

        except Exception as e:
            await message.reply_text(f"<b>Error:</b>\n<code>{e}</code>", True, parse_mode="html")
            LOGGER(__name__).error(e)
        return
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random.choice(PHOTO),
        caption=Translation.START_TEXT.format(
                message.from_user.mention, DEV_USERNAME),
        reply_markup=InlineKeyboardMarkup([[
              InlineKeyboardButton('➕ Add Me To Your Groups ➕', url='http://t.me/donlee_robot?startgroup=true')
              ],[
              InlineKeyboardButton(GROUP, url=HAAAAAAAAA),
              InlineKeyboardButton(CHANNEL, url=CHANNEL_LINK)
              ],[
              InlineKeyboardButton('ℹ️ Help', callback_data='help'),
              InlineKeyboardButton('😊 About', callback_data='about')
              ]]
        ),
        parse_mode="html",
        reply_to_message_id=message.message_id
    )


@DonLee_Robot.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
    await message.reply_photo(
        photo=random.choice(PHOTO),
        caption=Translation.HELP_TEXT.format(
                message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                         InlineKeyboardButton("Filter♂️", callback_data="filter1"),
                         InlineKeyboardButton("AutoFilter♂️", callback_data="autofilter1")
                    ],
                    [
                         InlineKeyboardButton("Extra Mode♂️", callback_data="info"),
                         InlineKeyboardButton("Connection♂️", callback_data="connection")
                    ],
                    [
                         InlineKeyboardButton("🤠 Status 🤠", callback_data="ooooooooo")
                    ],
                    [
                         InlineKeyboardButton("🏕️ Home", callback_data="start"),
                         InlineKeyboardButton("🗑️ Close 🗑️", callback_data="close"),
                         InlineKeyboardButton("About 🔥", callback_data="about")

                    ]
                ]
            )
        )

@DonLee_Robot.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
    userbot = await bot.get_me()
    await message.reply_photo(
        photo=random.choice(PHOTO),
        caption=Translation.ABOUT_TEXT.format(userbot.username, DEV_USERNAME, DEV_NAME, userbot.username),
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                         InlineKeyboardButton
                             (
                                 "📦 Source", callback_data="source"
                             ),
                         InlineKeyboardButton
                             (
                                 "Dev 🤠", callback_data="devmuhammed"
                             )
                    ],
                    [
                         InlineKeyboardButton
                             (
                                 "🏕️ Home", callback_data="start"
                             ),
                         InlineKeyboardButton
                             (
                                 "Close 🗑️", callback_data="close"
                             )
                    ]
                ]
            )
        )

@DonLee_Robot.on_message(filters.command(["subscribe", "sub"]) & filters.private, group=1)
async def sub(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
    await message.reply_photo(
        photo=random.choice(PHOTO),
        caption=Translation.SUB_TEXT,
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                         InlineKeyboardButton
                             (                                 
                                 "📣Group", url="t.me/mo_tech_group"
                             ),
                         InlineKeyboardButton
                             (
                                 "📢Channel", url="t.me/mo_tech_yt"
                             )
                    ],
                    [
                         InlineKeyboardButton
                             (
                                 "😟 Build a New Bot 😟", url="https://youtu.be/NrbMc93aCzA"
                             )
                    ],
                    [
                         InlineKeyboardButton
                             (
                                 "💥Subscribe youtube Channel💥", url="https://www.youtube.com/c/MoTech_YT"
                             )
                    ],
                    [
                         InlineKeyboardButton
                             (
                                 "🗑️ Close 🗑️", callback_data="close"
                             )
                    ]
                ]
            )
        )


      
@DonLee_Robot.on_message(filters.private & filters.command(["broadcast"]) & filters.reply)
async def broadcast_(c, m):
    print("broadcasting......")
    if m.from_user.id not in OWNER_ID:
        await c.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.message_id,
            revoke=True
        )
        return
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    
    out = await m.reply_text(
        text = f"Broadcast initiated! You will be notified with log file when all the users are notified."
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    
    broadcast_ids[broadcast_id] = dict(
        total = total_users,
        current = done,
        failed = failed,
        success = success
    )
    
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            
            sts, msg = await send_msg(
                user_id = int(user['id']),
                message = broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            
            if sts == 200:
                success += 1
            else:
                failed += 1
            
            if sts == 400:
                await db.delete_user(user['id'])
            
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current = done,
                        failed = failed,
                        success = success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    
    await asyncio.sleep(3)
    
    await out.delete()
    
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    
    await aiofiles.os.remove('broadcast.txt')



@DonLee_Robot.on_message(filters.private & filters.command(["status", "stats"]))
async def status(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    total_users = await db.total_users_count()
    await update.reply_text(
        text=Translation.STATUS_TEXT.format(total_users),
        quote=True,
        disable_web_page_preview=True
    )


@DonLee_Robot.on_message(filters.command(["settings"]) & filters.group, group=1)
async def settings(bot, update):
    
    chat_id = update.chat.id
    user_id = update.from_user.id if update.from_user else None
    global VERIFY

    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)): # Checks if user is admin of the chat
        return
    
    bot_info = await bot.get_me()
    bot_first_name= bot_info.first_name
    
    text =f"<u>{bot_first_name}'s</u> Settings Pannel.....\n"
    text+=f"\nYou Can Use This Menu To Change Connectivity And Know Status Of Your Every Connected Channel, Change Filter Types, Configure Filter Results"
    
    buttons = [[
        InlineKeyboardButton("📣 Channels 📣", callback_data=f"channel_list({chat_id})")
        ],[
        InlineKeyboardButton("📚 Filter Types 📚", callback_data=f"types({chat_id})")
        ],[
        InlineKeyboardButton("🛠 Configure 🛠", callback_data=f"config({chat_id})")
        ],[
        InlineKeyboardButton("👩‍👦‍👦 Group Status", callback_data=f"status({chat_id})"), 
        InlineKeyboardButton("🤖 Bot Status", callback_data=f"about({chat_id})")
        ],[
        InlineKeyboardButton("🔐 Close 🔐", callback_data="close")
        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_photo (
        chat_id=chat_id,
        photo=random.choice(PHOTO),
        caption=text, 
        reply_markup=reply_markup, 
        parse_mode="html",
        reply_to_message_id=update.message_id
    )




