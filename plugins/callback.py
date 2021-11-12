import math
import json
import time
import shutil
import heroku3
import requests
import os, ast
from pyrogram import filters, Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from translation import Translation
from donlee_robot.donlee_robot import DonLee_Robot
from database import all_connections, active_connection, if_active, delete_connection, make_active, make_inactive, del_all, find_filter, Database, add_user, all_users, humanbytes, filter_stats
from config import start_uptime, DEV_USERNAME, DEV_NAME, BOT_USERNAME, GROUP, GROUP_LINK, CHANNEL_LINK, CHANNEL
db = Database()

AA = f"t.me/{GROUP_LINK}"

@DonLee_Robot.on_callback_query()
async def cb_handler(client, query):

    if query.data == "close":
        await query.message.delete()
 
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return

        elif (chat_type == "group") or (chat_type == "supergroup"):
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in Config.AUTH_USERS):    
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!",show_alert=True)
    
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type
        
        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif (chat_type == "group") or (chat_type == "supergroup"):
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in Config.AUTH_USERS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Thats not for you!!",show_alert=True)


    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        act = query.data.split(":")[3]
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnectbot"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}:{title}"),
                InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
            return
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return

    elif "disconnectbot" in query.data:
        await query.answer()

        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
            return
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
            return
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return
    
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                if active:
                    act = " - ACTIVE"
                else:
                    act = ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{title}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
   
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert,show_alert=True)

    elif query.data == "start":
        await query.message.edit_text(Translation.START_TEXT.format(query.from_user.mention, DEV_USERNAME), reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{BOT_USERNAME}?startgroup=true')
                   ],
                   [
                       InlineKeyboardButton(GROUP, url=AA),
                       InlineKeyboardButton(CHANNEL, url=CHANNEL_LINK)
                   ],
                   [
                       InlineKeyboardButton('ℹ️ Help', callback_data='help'),
                       InlineKeyboardButton('😊 About', callback_data='about')
                   ]
               ]
           )  
       )
    elif query.data == "help": 
        await query.message.edit_text(Translation.HELP_TEXT, reply_markup=InlineKeyboardMarkup(
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
                         InlineKeyboardButton(" About 🔥", callback_data="about")
                   ]
               ]
           )  
       )
    elif query.data == "about":   
        await query.message.edit_text(Translation.ABOUT_TEXT.format(BOT_USERNAME, DEV_USERNAME, DEV_NAME, BOT_USERNAME), reply_markup=InlineKeyboardMarkup(
               [
                   [
                         InlineKeyboardButton("📦 Source", callback_data="source"),
                         InlineKeyboardButton("Dev 🤠", callback_data="devmuhammed")
                   ],
                   [
                         InlineKeyboardButton("🏕️ Home", callback_data="start"),
                         InlineKeyboardButton("Close 🗑️", callback_data="close")
                   ]
               ]
           )
       )
    elif query.data == "autofilter1":
        await query.message.edit_text(Translation.AUTOFILTER_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("➡️ Next Page ➡️", callback_data="autofilter2")
                   ],
                   [
                       InlineKeyboardButton("🔙 Back 🔙", callback_data="help")
                   ]
               ]
           )
       )
    elif query.data == "autofilter2":
        await query.message.edit_text(Translation.AUTOFILTER_TEXT2, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("🔙 Back Page 🔙", callback_data="autofilter1")
                   ]
               ]
           )
       )
    elif query.data == "filter1":
        await query.message.edit_text(Translation.FILTER_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("🔙 Back 🔙", callback_data="help")
                   ]
               ]
           )
       )
    elif query.data == "connection":
        await query.message.edit_text(Translation.CONNECTION_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("🔙 Back 🔙", callback_data="help")
                   ]
               ]
           )
       )
    elif query.data == "info":
        await query.message.edit_text(Translation.INFORMATION_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("🔙 BacK", callback_data="help"),
                       InlineKeyboardButton("🙎‍♂️ Admins", callback_data="groupadmin")
                   ]
               ]
           )
       )
    elif query.data == "groupadmin":
        await query.message.edit_text(Translation.GROUP_ADMIN_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("🔙 Back 🔙", callback_data="info")
                   ]
               ]
           )
       )
    elif query.data == "source":
        await query.message.edit_text(Translation.SOURCE_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('☢️Frok', url='https://github.com/PR0FESS0R-99/DonLee-Robot-V2/fork'),
                       InlineKeyboardButton('🌟Star', url='https://github.com/PR0FESS0R-99/DonLee-Robot-V2/stargazers')
                   ],
                   [
                       InlineKeyboardButton('🏵Repo', url='https://youtu.be/NrbMc93aCzA'),
                       InlineKeyboardButton('🧩Deplow', url='https://youtu.be/NrbMc93aCzA')
                   ],
                   [
                       InlineKeyboardButton("🔙 Back 🔙", callback_data="about")
                   ]
               ]
           )
       )
    elif query.data == "ooooooooo":
        total_users = await db.total_users_count()
        chats, filters = await filter_stats()
        uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - start_uptime))
        await query.message.edit_text(Translation.DYNO_TEXT.format(total_users, chats, filters, uptime), reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("🔙 Back", callback_data="help"),
                       InlineKeyboardButton("🔃", callback_data="ooooooooo")
                   ]
               ]
           )
       )
    elif query.data == "devmuhammed":
        await query.message.edit_text(Translation.DEV_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("🔙 Back", callback_data="about"),
                       InlineKeyboardButton("🥳 Credits", callback_data="creditsmuhammmed")
                   ]
               ]
           )
       )
    elif query.data == "creditsmuhammmed":
        await query.message.edit_text(Translation.CREDITS_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("TroJanzHEX", url="https://github.com/TroJanzHEX"),
                       InlineKeyboardButton("Use", url="https://github.com/TroJanzHEX/Unlimited-Filter-Bot")
                   ],
                   [
                       InlineKeyboardButton("CrazyBotsz", url="https://github.com/CrazyBotsz"),
                       InlineKeyboardButton("Use", url="https://github.com/CrazyBotsz/Adv-Auto-Filter-Bot-V2")
                   ],
                   [
                       InlineKeyboardButton("bughunter0", url="https://github.com/bughunter0"),
                       InlineKeyboardButton("Use", url="https://github.com/bughunter0/ban-bot")
                   ],
                   [
                       InlineKeyboardButton("Pr0fess0r-99", url="https://github.com/Pr0fess0r-99"),
                       InlineKeyboardButton("Use", url="https://github.com/Pr0fess0r-99/Auto-Welcome-Bot")
                   ],
                   [
                       InlineKeyboardButton("EvamariaTG", url="https://github.com/EvamariaTG"),
                       InlineKeyboardButton("Use", url="https://github.com/EvamariaTG/EvaMaria")
                   ],
                   [
                       InlineKeyboardButton("🔙 back 🔙", callback_data="devmuhammed")
                   ]
               ]
           )
       )
    elif query.data == "creditsabout":
        await query.message.edit_text(Translation.CREDITS_TEXT, reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("TroJanzHEX", url="https://github.com/TroJanzHEX"),
                       InlineKeyboardButton("Use", url="https://github.com/TroJanzHEX/Unlimited-Filter-Bot")
                   ],
                   [
                       InlineKeyboardButton("CrazyBotsz", url="https://github.com/CrazyBotsz"),
                       InlineKeyboardButton("Use", url="https://github.com/CrazyBotsz/Adv-Auto-Filter-Bot-V2")
                   ],
                   [
                       InlineKeyboardButton("bughunter0", url="https://github.com/bughunter0"),
                       InlineKeyboardButton("Use", url="https://github.com/bughunter0/ban-bot")
                   ],
                   [
                       InlineKeyboardButton("Pr0fess0r-99", url="https://github.com/Pr0fess0r-99"),
                       InlineKeyboardButton("Use", url="https://github.com/Pr0fess0r-99/Auto-Welcome-Bot")
                   ],
                   [
                       InlineKeyboardButton("EvamariaTG", url="https://github.com/EvamariaTG"),
                       InlineKeyboardButton("Use", url="https://github.com/EvamariaTG/EvaMaria")
                   ],
                   [
                       InlineKeyboardButton("🔙 back 🔙", callback_data="source")
                   ],
                   [
                       InlineKeyboardButton("🏕️ Home", callback_data="start"),
                       InlineKeyboardButton(" About 🔥", callback_data="about"),
                       InlineKeyboardButton("Close 🗑️", callback_data="close")
                   ]
               ]
           )
       )
