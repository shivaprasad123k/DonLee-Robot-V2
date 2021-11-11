import pyrogram
import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message, User, InlineKeyboardMarkup, InlineKeyboardButton
from donlee_robot.donlee_robot import DonLee_Robot
from config import FORCE_CHANNEL, SAVE_USER, DEV_USERNAME, WELCOME_BUTTON_NAME, CUSTOM_WELCOME_TEXT, CUSTOM_WELCOME

# f"👋Hy {mention} Welcome To {groupname}"
Url = f"t.me/{FORCE_CHANNEL}"
WELCOME_BUTTONS = [[ InlineKeyboardButton(WELCOME_BUTTON_NAME, url=Url)]]    


@DonLee_Robot.on_message(filters.command('id') & (filters.private | filters.group))
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"Your ID : `{user_id}`",
            parse_mode="md",
            quote=True
        )
    elif (chat_type == "group") or (chat_type == "supergroup"):
        user_id = message.from_user.id
        chat_id = message.chat.id
        if message.reply_to_message:
            reply_id = f"Replied User ID : `{message.reply_to_message.from_user.id}`"
        else:
            reply_id = ""
        await message.reply_text(
            f"Your ID : `{user_id}`\nThis Group ID : `{chat_id}`\n\n{reply_id}",
            parse_mode="md",
            quote=True
        )   


@DonLee_Robot.on_message(filters.command('info') & (filters.private | filters.group))
async def showinfo(client, message):
    try:
        cmd, id = message.text.split(" ", 1)
    except:
        id = False
        pass

    if id:
        if (len(id) == 10 or len(id) == 9):
            try:
                checkid = int(id)
            except:
                await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
                return
        else:
            await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
            return           

        if SAVE_USER == "yes":
            name, username, dcid = await find_user(str(id))
        else:
            try:
                user = await client.get_users(int(id))
                name = str(user.first_name + (user.last_name or ""))
                username = user.username
                dcid = user.dc_id
            except:
                name = False
                pass

        if not name:
            await message.reply_text("__USER Details not found!!__", quote=True, parse_mode="md")
            return
    else:
        if message.reply_to_message:
            name = str(message.reply_to_message.from_user.first_name\
                    + (message.reply_to_message.from_user.last_name or ""))
            id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            dcid = message.reply_to_message.from_user.dc_id
        else:
            name = str(message.from_user.first_name\
                    + (message.from_user.last_name or ""))
            id = message.from_user.id
            username = message.from_user.username
            dcid = message.from_user.dc_id
    
    if not str(username) == "None":
        user_name = f"@{username}"
    else:
        user_name = "none"

    await message.reply_text(
        f"<b>👨‍💼Name</b> : {name}\n\n"
        f"<b>📃User ID</b> : <code>{id}</code>\n\n"
        f"<b>👤Username</b> : {user_name}\n\n"
        f"<b>🔐Permanant USER link</b> : <a href='tg://user?id={id}'>Click here!</a>\n\n"
        f"<b>📑DC ID</b> : {dcid}\n\n",
        quote=True,
        parse_mode="html"
    ) 

@DonLee_Robot.on_message(filters.group & filters.forwarded)
async def forward(bot, message):
        await message.delete()

@DonLee_Robot.on_message(filters.group & filters.via_bot)
async def inline(bot, message):
        await message.delete()

@DonLee_Robot.on_message(filters.new_chat_members)
async def auto_welcome(bot: DonLee_Robot, msg: Message):
#   from PR0FESS0R-99 import Auto-Welcome-Bot
#   from PR0FESS0R-99 import ID-Bot
#   first = msg.from_user.first_name
#   last = msg.from_user.last_name
#   mention = msg.from_user.mention
#   username = msg.from_user.username
#   id = msg.from_user.id
#   group_name = msg.chat.title
#   group_username = msg.chat.username
#   button_name = os.environ.get("WELCOME_BUTTON_NAME", name_button)
#   button_link = os.environ.get("WELCOME_BUTTON_LINK", link_button)
#   welcome_text = f"Hey {mention}\nWelcome To {group_name}"
#   WELCOME_TEXT = os.environ.get("WELCOME_TEXT", welcome_text)
    print("Welcome Message Activate")
#   YES = "True"
#   NO = "False"
#   HOOOO = CUSTOM_WELCOME
#   BUTTON = bool(os.environ.get("CUSTOM_WELCOME"))
    if CUSTOM_WELCOME == "yes":
        Auto_Delete=await msg.reply_text(text=CUSTOM_WELCOME_TEXT.format(
            mention = msg.from_user.mention,
            groupname = msg.chat.title
            ),
        reply_markup=InlineKeyboardMarkup(WELCOME_BUTTONS)
        )
        await asyncio.sleep(60) # in seconds
        await Auto_Delete.delete()
    else:
        await msg.delete()



@DonLee_Robot.on_message((filters.command(["report"]) | filters.regex("@admins") | filters.regex("@admin")) & filters.group)
async def report(bot, message):
    if message.reply_to_message:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        admins = await bot.get_chat_members(chat_id=chat_id, filter="administrators")
        success = False
        report = f"Reporter : {mention} ({reporter})" + "\n"
        report += f"Message : {message.reply_to_message.link}"
        for admin in admins:
            try:
                reported_post = await message.reply_to_message.forward(admin.user.id)
                await reported_post.reply_text(
                    text=report,
                    chat_id=admin.user.id,
                    disable_web_page_preview=True
                )
                success = True
            except:
                pass
        if success:
            await message.reply_text("**Reported to Admins!**")


@DonLee_Robot.on_message(filters.command(["ban"]))
async def ban(bot, message):
    chatid = message.chat.id
    if message.reply_to_message:
        admins_list = await bot.get_chat_members(
            chat_id=chatid, filter="administrators"
        )
        admins = []
        for admin in admins_list:
            id = admin.user.id
            admins.append(id)
        userid = message.from_user.id
        if userid in admins:
            user_to_ban = message.reply_to_message.from_user.id
            if user_to_ban in admins:
                await message.reply(text="Think he is Admin, Can't Ban Admins")
            else:
                try:
                    await bot.kick_chat_member(chat_id=chatid, user_id=user_to_ban)
                    await message.reply_text(
                        f"Bye {message.reply_to_message.from_user.mention}"
                    )
                except Exception as error:
                    await message.reply_text(f"{error}")
        else:
            await message.reply_text("Nice try, But wrong move..")
            return
    else:
        return


@DonLee_Robot.on_message(filters.command(["unban"]))
async def ban(bot, message):
    chatid = message.chat.id
    if message.reply_to_message:
        admins_list = await bot.get_chat_members(
            chat_id=chatid, 
            filter="administrators"
        )
        admins = []
        for admin in admins_list:
            id = admin.user.id
            admins.append(id)
        userid = message.from_user.id
        if userid in admins:
            user_to_ban = message.reply_to_message.from_user.id
            if user_to_unban in admins:
                await message.reply(text="Think he is Admin, Can't Ban Admins")
            else:
                try:
                    await bot.unban_chat_member(chat_id=chatid, user_id=user_to_unban)
                    await message.reply_text(
                        f"welcome {message.reply_to_message.from_user.mention}"
                    )
                except Exception as error:
                    await message.reply_text(f"{error}")
        else:
            await message.reply_text("Nice try, But wrong move..")
            return
    else:
        return

@DonLee_Robot.on_message(filters.channel & filters.text | filters.media )
async def tag(client, message):
    await message.copy(message.chat.id)
