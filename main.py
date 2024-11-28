import qrcode.constants
from telethon import TelegramClient, events , functions,types,Button
from telethon.tl.types import ChannelParticipantsAdmins,ChannelParticipantsSearch,Chat, Channel,ChatPhoto,ChatBannedRights
from telethon.tl.functions.messages import ImportChatInviteRequest,EditMessageRequest,CreateChatRequest, AddChatUserRequest,GetHistoryRequest,SendMessageRequest,SendInlineBotResultRequest
from telethon.tl.functions.channels import GetFullChannelRequest,EditAdminRequest, InviteToChannelRequest,GetParticipantsRequest,CreateChannelRequest,EditBannedRequest
from telethon.tl.types import Channel, Chat, ChannelParticipant,ChatAdminRights,PeerChannel,ChannelParticipantsRecent,MessageMediaPhoto, MessageMediaDocument, MessageMediaContact, MessageMediaGeo, MessageMediaVenue,ChannelParticipantsKicked,ChannelParticipantsBots,ChannelParticipantsBanned,InputPeerUser,InputBotInlineMessageID,UserStatusOnline
from datetime import datetime
from telethon.tl.types import (
    UserStatusOnline,
    UserStatusOffline,
    UserStatusRecently,
    UserStatusLastWeek,
    UserStatusLastMonth
)
from googletrans import Translator
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from art import text2art
from io import BytesIO
from PIL import Image
from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which
from bs4 import BeautifulSoup
import base64
import asyncio
import io
import time
import qrcode
import re
import json
import os
import math
import requests
import random
import psutil
import logging
import pytz

telethon_api_id = "20361782"
telethon_api_hash = "897076701aa60c97f24f2fe4926444a7"

client = TelegramClient("telethon_session", telethon_api_id,telethon_api_hash)

OWNER_ID = 7124786301 

def is_owner(event):
    return event.sender_id == OWNER_ID

# comlist komutu
@client.on(events.NewMessage(pattern=r'\.komut'))
async def comlist(event):
    if not is_owner(event):
        return
    commands = """
    ```
**🛠 Telethon Listi:**
1. 🟢 **.alive** - bot aktiv komutu 
2. ℹ️ **.infoqrup** - qrup haqqında informasiya 
3. 👑 **.uspromote** - useri admin etmək
6. ⚠️ **.usdemote** - userin adminliyini almaq
8. 📇 **.addkk** - kontakta əlavə etmək (istifadə: reply + .addkk ad)
9. 🗑 **.allkkdel** - toplu kontakt silmək
10. 🎨 **.asc <mətin>** - sözləri ascii fonta çevirmək 
12. 🌐 **.lang <mətin>** - cümlə və sözləri tərcümə etmək
13. 🇬🇧 **.langEng <mətin>** - cümlə və sözləri ingilis dilinə çevirmək
14. 📈 **.curren** - valyuta çevirici
15. π **.riyaz** - riyaziyyat misalları həll etmək
17. 🎵 **.liriks** - mahnı sözləri tapmaq
18. 📜 **.adminl** - qrupun admin listi
19. 👥 **.tektag** - tək-tək tag etmək
20. 🛑 **.stoptag** - tag etməni dayandır
22. 📞 **.kk (say) [isim]** - avtoamtik random kontakta əlavə etmək
24. 🔄 **.raid** - basqın
24. ❌ **.allban** - avtomatik bütün istifadəçiləri ban etmək
25. 🔁 **.sback** - sözləri tərs çevirmək
26. 🖼 **.profilkolaj** - profilləri birləşdirmə
26. ⛔️ **.bansayi** - qrupdakı ban və fban sayı
32. ❓ **.tapmaca** - tapmaca oyunu başladır
32. 🛑 **.stopoyun** - tapmaca oyununu dayandırır
33. ⏱ **.songorulme** - istifadəçinin son görülmə vaxtını göstərir
34. 🎧 **.sesler** - Səs effektləri listini göstərir
35. 📥 **.add [səs adı]** - səsə reply ataraq səs listinə əlavə et
36. 😁 **$[ses adı]** - Ses listinden bir sesi $ bu işarə ilə göndər
37. 🧬 **.klon** - profilleri klonla
38. ↩️ **.back** - öz profilinə qayıt
39. 💣 **.ride** - basqın komutu istifadə: .ride [söz]
40. ⏹ **.stopride** - basqını dayandır
41. 🕕 **.tname** - ada saat əlavə et
42. **.filter** - reply ataraq filter əlavə et
43. **.filtersil** - (.filtersil [soz]) əlavə olunan filteri sil
44. **.filters** - bütün filterlərə bax
45. **.delfilterall** - bütün filterləri sil
```
    """
    await event.reply(commands)

# aktiv komutu

@client.on(events.NewMessage(pattern=r'\.alive'))
async def active_command(event):
    await event.edit(f"⚝ `༒ℍİ𝕂𝕆༒ userbot aktivdir...`")

# qrup info

@client.on(events.NewMessage(pattern=r'\.infoqrup'))
async def handler(event):
    if not is_owner(event):
        return
    chat = await event.get_chat()

    if isinstance(chat, (Channel, Chat)):
        try:
            full_chat = await client(GetFullChannelRequest(channel=chat))

            group_title = chat.title
            group_username = f"@{chat.username}" if chat.username else "None"
            group_id = chat.id
            members_count = full_chat.full_chat.participants_count

            # En eski mesajı al
            messages = await client.get_messages(chat.id, limit=1, reverse=True)
            if messages:
                oldest_message = messages[0]
                created_date = oldest_message.date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                created_date = "Unknown"

            bots_count = 0
            admins_count = 0
            creator = None

            async for participant in client.iter_participants(chat.id):
                if participant.bot:
                    bots_count += 1
                elif isinstance(participant, ChannelParticipant):
                    if participant.admin_rights and participant.admin_rights.is_creator:
                        creator = participant
                    if participant.admin_rights and participant.admin_rights.is_admin:
                        admins_count += 1

            if creator:
                creator_name = creator.user.first_name
                creator_username = f"@{creator.user.username}" if creator.user.username else "None"
                creator_info = f"[{creator_name}](tg://user?id={creator.user.id}) ({creator_username})"
            else:
                creator_info = "Unknown"

            group_details = (
                f"**Group Information**\n"
                f"Initial Name: {group_title}\n"
                f"Tag: {group_username}\n"
                f"Group ID: {group_id}\n"
                f"Group Creation Date: {created_date}\n"
                f"Member Count: {members_count}\n"
                f"Bot Count: {bots_count}\n"
                f"Admin Count: {admins_count}\n"
            )

            await event.reply(group_details)
        except Exception as e:
            await event.reply(f"Failed to retrieve group info. Error: {str(e)}")
    else:
        await event.reply("This command can only be used in groups or supergroups.")

# istifadəçi yetkiləndirmə və ya alma


admin_rights = ChatAdminRights(
    delete_messages=True,
    manage_call=True,  
    invite_users=True,
    change_info=False,
    ban_users=False,
    pin_messages=False,
    add_admins=False
)

no_rights = ChatAdminRights(
    delete_messages=False,
    manage_call=False,
    invite_users=False,
    change_info=False,
    ban_users=False,
    pin_messages=False,
    add_admins=False
)

@client.on(events.NewMessage(pattern=r'\.uspromote'))
async def promote_user(event):
    if not is_owner(event):
        return
    if not event.is_group:
        await event.reply("**Bu komutu sadece qruplarda istifadə edə bilərsiniz**")
        return

    user = None
    custom_title = ""

    if event.is_reply:
        reply_message = await event.get_reply_message()
        user = await client.get_entity(reply_message.from_id)
        custom_title = event.message.text.split(' ', 1)[1] if len(event.message.text.split(' ', 1)) > 1 else ""
    else:
        try:
            user_data = event.message.text.split(' ', 2)
            user = await client.get_entity(user_data[1])
            custom_title = user_data[2] if len(user_data) > 2 else ""
        except (IndexError, ValueError):
            await event.reply("**Zəhmət olmasa keçərli bir istifadəçi ID'si, etiket və ya mesaja cavab olaraq istifadə edin**")
            return

    if not user:
        await event.reply("**İstifadəçi tapılmadı**")
        return

    permissions = await client.get_permissions(event.chat_id, 'me')
    if permissions.is_admin:
        await client(EditAdminRequest(
            channel=PeerChannel(event.chat_id),
            user_id=user.id,
            admin_rights=admin_rights,
            rank=custom_title
        ))
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        await event.reply(f"**İstifadəçi {mention} indi admindir**")
    else:
        await event.reply("**Sizin bu qrupda istifadəçini admin etmə icazəniz yoxdur**")

@client.on(events.NewMessage(pattern=r'\.usdemote'))
async def demote_user(event):
    if not is_owner(event):
        return
    if not event.is_group:
        await event.reply("**Bu komutu sadece qruplarda istifadə edə bilərsiniz**")
        return

    user = None
    if event.is_reply:
        reply_message = await event.get_reply_message()
        user = await client.get_entity(reply_message.from_id)
    else:
        try:
            user = await client.get_entity(event.message.text.split()[1])
        except (IndexError, ValueError):
            await event.reply("**Zəhmət olmasa keçərli bir istifadəçi ID'si, etiket və ya mesaja cavab olaraq istifadə edin**")
            return

    if not user:
        await event.reply("**İstifadəçi tapılmadı**")
        return

    permissions = await client.get_permissions(event.chat_id, 'me')
    if permissions.is_admin:
        await client(EditAdminRequest(
            channel=PeerChannel(event.chat_id),
            user_id=user.id,
            admin_rights=no_rights,
            rank=""  # Kullanıcının yönetici olarak atanmadığını göstermek için boş bırakıyoruz
        ))
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        await event.reply(f"**İstifadəçi {mention} artıq admin deyil**")
    else:
        await event.reply("**Sizin bu qrupda istifadəçini adminlikdən çıxarma icazəniz yoxdur**")

# tek kontakta salma

@client.on(events.NewMessage(pattern=r'\.addkk'))
async def setcc(event):
    if not is_owner(event):
        return
    if event.is_reply:
        reply_message = await event.get_reply_message()
        user = await client.get_entity(reply_message.from_id)
        
        command_parts = event.message.text.split(' ', 1)
        if len(command_parts) > 1:
            new_name = command_parts[1]
        else:
            new_name = user.first_name
        
        try:
            await client(functions.contacts.AddContactRequest(
                id=user.id,
                first_name=new_name,
                last_name='',
                phone=''
            ))
            await event.edit(f"**{user.first_name} artıq kontaktdır və adı {new_name} olaraq dəyişdirildi**")
        except Exception as e:
            await event.edit(f"**Xəta baş verdi:** {str(e)}")
    
    else:
        command_parts = event.message.text.split(' ', 2)
        if len(command_parts) < 3:
            await event.edit("**Kullanıcı ID/etiket və yeni ad daxil edilməlidir**")
            return
        
        identifier = command_parts[1]
        new_name = command_parts[2]
        
        try:
            user = await client.get_entity(identifier)
            await client(functions.contacts.AddContactRequest(
                id=user.id,
                first_name=new_name,
                last_name='',
                phone=''
            ))
            await event.edit(f"**{user.first_name} artıq kontaktdır və adı {new_name} olaraq dəyişdirildi**")
        except Exception as e:
            await event.edit(f"**Xəta baş verdi:** {str(e)}")

# toplu kontakt silme

@client.on(events.NewMessage(pattern=r'\.allkkdel'))
async def delkontaktall(event):
    if not is_owner(event):
        return
    try:
        contacts = await client(functions.contacts.GetContactsRequest(hash=0))
        if not contacts.users:
            await event.edit("**Heç bir kontakt tapılmadı**")
            return
        
        for user in contacts.users:
            try:
                await client(functions.contacts.DeleteContactsRequest(id=[user.id]))
                await event.edit(f"**{user.first_name} adlı istifadəçi silindi**")
                time.sleep(2)  
            except Exception as e:
                if "A wait of" in str(e):
                    wait_time = int(''.join(filter(str.isdigit, str(e))))
                    await event.edit(f"**Silmə limitinə çatıldı \n{wait_time} saniyə gözləmə**")
                    time.sleep(wait_time)
                else:
                    await event.edit(f"**{user.first_name} adlı istifadəçi silinərkən xəta baş verdi:** {str(e)}")
                    continue
        
        await event.edit("**Bütün kontaktlar silindi**")
    except Exception as e:
        await event.edit(f"**Xəta baş verdi:** {str(e)}")

# yazını ascii etmək

@client.on(events.NewMessage(pattern=r'\.asc (.+)'))
async def ascii(event):
    if not is_owner(event):
        return
    if event.is_reply:
        replied_message = await event.get.reply_message()
        text = replied_message.message
    else:
        text = event.pattern_match.group(1)

    ascii_art = text2art(text)

    await event.edit(f"```\n{ascii_art}\n```", parse_mode = 'markdown')

# bütün dilləri azərbaycan dilinə çevirmə

translator = Translator()

@client.on(events.NewMessage(pattern=r'\.lang( .+|$)'))
async def translate_text(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        text_to_translate = reply_message.text
    else:
        if len(event.message.text.split()) < 2:
            await event.reply("Usage: .translate <text> or reply to a message with .translate")
            return
        text_to_translate = event.message.text.split(maxsplit=1)[1]
    
    try:
        translated = translator.translate(text_to_translate, dest='az')
        translated_text = translated.text

        await event.reply(f"✅ 𝚃𝚛𝚊𝚗𝚜𝚕𝚊𝚝𝚒𝚘𝚗 𝙲𝚘𝚖𝚙𝚕𝚎𝚝𝚎\n\n`Original word`: **{text_to_translate}**\n`Translated word`: **{translated_text}**")
    
    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")

# bütün dilləri İngilis dilinə çevirmə

@client.on(events.NewMessage(pattern=r'\.langEng( .+|$)'))
async def translate_text_eng(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        text_to_translate = reply_message.text
    else:
        if len(event.message.text.split()) < 2:
            await event.reply("Usage: .translateEng <text> or reply to a message with .translateEng")
            return
        text_to_translate = event.message.text.split(maxsplit=1)[1]

    try:
        translated = translator.translate(text_to_translate, dest='en')
        translated_text = translated.text

        await event.reply(f"✅ 𝚃𝚛𝚊𝚗𝚜𝚕𝚊𝚝𝚒𝚘𝚗 𝙲𝚘𝚖𝚙𝚕𝚎𝚝𝚎\n\n`Original word`: **{text_to_translate}**\n`Translated word`: **{translated_text}**")
    
    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")


# riyaziyyat hell etme kodlari

@client.on(events.NewMessage(pattern=r'\.riyaz( .+|$)'))
async def calculate_expression(event):
    try:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            expression = reply_message.text
        else:
            args = event.message.text.split(maxsplit=1)
            if len(args) < 2:
                await event.reply("Usage: .cal <expression> or reply to a message with .cal")
                return
            expression = args[1]

        expression = expression.replace("√", "math.sqrt")

        result = eval(expression, {"__builtins__": None}, {"math": math})

        await event.reply(f"Cavab:\n{result}")

    except Exception as e:
        await event.reply(f"XƏTA: {str(e)}")

# valyuta ceviren

def stylize_text(text):
    return f"✨ **{text}** ✨"

@client.on(events.NewMessage(pattern=r'\.curren'))
async def currency(event):
    try:
        text = event.message.text.split(" ", 1)
        if len(text) < 2:
            await event.reply(stylize_text("Düzgün format: `.valyuta məbləğ FROM TO` (məsələn, `.valyuta 100 USD EUR`)"))
            return
        
        amount, from_currency, to_currency = text[1].split(" ")
        amount = float(amount)
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url).json()

        if response.get("error"):
            await event.reply(stylize_text(f"Xəta: {response['error']}"))
            return

        if to_currency not in response['rates']:
            await event.reply(stylize_text(f"Dəyişmə dərəcəsi tapılmadı: {to_currency}"))
            return

        rate = response['rates'][to_currency]
        converted_amount = amount * rate
        
        await event.reply(stylize_text(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"))

    except ValueError:
        await event.reply(stylize_text("Yanlış məbləğ. Zəhmət olmasa düzgün məbləğ daxil edin."))
    except IndexError:
        await event.reply(stylize_text("Düzgün format: `.valyuta məbləğ FROM TO` (məsələn, `.valyuta 100 USD EUR`)"))
    except Exception as e:
        await event.reply(stylize_text(f"Xəta baş verdi: {str(e)}"))

# mahni sozu tapma

GENIUS_API = "FdiG8NMlpEVOW3fJnaJqW7Vom-8p9lUauP_jNuA5PLbX3L-kDznZlIghV2Opiooz"

def get_lyrics(song_title):
    headers = {
        'Authorization': f'Bearer {GENIUS_API}'
    }
    search_url = 'https://api.genius.com/search'
    params = {
        'q': song_title
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
   
    try:
        song_path = data['response']['hits'][0]['result']['path']
        lyrics_url = f'https://genius.com{song_path}'
       
        lyrics_response = requests.get(lyrics_url)
        soup = BeautifulSoup(lyrics_response.text, 'html.parser')
      
        lyrics_div = soup.find('div', class_='lyrics')
        if lyrics_div:
            lyrics = lyrics_div.get_text(strip=True, separator="\n")
        else:
            lyrics_div = soup.find('div', class_=re.compile('Lyrics__Container'))
            if lyrics_div:
                lyrics = lyrics_div.get_text(strip=True, separator="\n")
            else:
                lyrics = "Mahnı sözləri tapılmadı."

        return f"🅒🅞🅛🅓 🅤🅢🅔🅡🅑🅞🅣\n\n{lyrics}"
        
    except IndexError:
        return "Mahnı sözləri tapılmadı."
    except Exception as e:
        return f"Xəta baş verdi: {str(e)}"

@client.on(events.NewMessage(pattern=r'\.liriks (.+)'))
async def lyrics(event):
    song_title = event.pattern_match.group(1)
    lyrics_text = get_lyrics(song_title)
    
    await event.reply(lyrics_text)

# admin listi

@client.on(events.NewMessage(pattern=r'\.adminl', outgoing=True))
async def adminlist_command(event):
    chat = await event.get_input_chat()
    admins = await client(GetParticipantsRequest(
        channel=chat,
        filter=ChannelParticipantsAdmins(),
        offset=0,
        limit=100,
        hash=0
    ))

    admin_list = []
    for admin in admins.participants:
        user = await client.get_entity(admin.user_id)
        custom_title = admin.rank if admin.rank else "No Title"
        admin_info = f"➤ [{user.first_name}](tg://user?id={user.id}): [{custom_title}]"
        admin_list.append(admin_info)

    if admin_list:
        admin_info_message = "**Qrupdakı Adminlər:**\n\n" + "\n".join(admin_list)
        admin_info_message += f"\n\n🜲 **Admin Sayı:** {len(admin_list)}"
    else:
        admin_info_message = "🚫 Bu qrupda admin yoxdur."

    await event.respond(admin_info_message, link_preview=False)

# etiketleme 

stop_labeling = False
labeling_task = None

async def label_users(event, label_text):
    global stop_labeling, labeling_task
    chat = await event.get_input_chat()
    
    participants = await client(GetParticipantsRequest(
        channel=chat,
        filter=ChannelParticipantsSearch(''),
        offset=0,
        limit=200,
        hash=0
    ))

    user_list = [p for p in participants.users if not p.bot]
    total_users = len(user_list)

    if total_users == 0:
        await event.reply("Bu qrupda heç bir iştirakçı yoxdur.")
        return

    random.shuffle(user_list)
    count = 0

    for user in user_list:
        if count >= 100 or stop_labeling:
            break

        if user.username:
            mention = f"@{user.username}"
        else:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
        
        message = f"{label_text} {mention}"

        try:
            await event.respond(message, link_preview=False)
            count += 1
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Xəta baş verdi: {str(e)}")

    if count == 0:
        await event.respond("Heç bir istifadəçi etiketlenmədi.")

@client.on(events.NewMessage(pattern=r'\.tektag', outgoing=True))
async def label_command(event): 
    if not is_owner(event):
        return
    await event.edit("**༒ℍİ𝕂𝕆༒ aktivləşdi... \nEtiketləmə başladılır**")
    global stop_labeling, labeling_task
    if labeling_task and not stop_labeling:
        await event.edit("Etiketleme artıq davam edir.")
        return

    if stop_labeling:
        stop_labeling = False  

    text = event.text.split(" ", 1)
    if len(text) < 2:
        await event.reply("Düzgün format: .label <mesaj>")
        return

    label_text = text[1]
    labeling_task = asyncio.create_task(label_users(event, label_text))

@client.on(events.NewMessage(pattern=r'\.stoptag', outgoing=True))
async def lstop_command(event):
    if not is_owner(event):
        return
    global stop_labeling, labeling_task
    if not stop_labeling:
        stop_labeling = True
        if labeling_task:
            labeling_task.cancel()
            labeling_task = None
        await event.edit("**Etiketləmə dayandırıldı**")
    else:
        await event.edit("Etiketləmə zatən dayandırılıb")

# random kontakta elave elemek

@client.on(events.NewMessage(pattern=r'\.kk (\d+) (.+)'))
async def handle_kontakt(event):
    if not is_owner(event):
        return
    try:
        count = int(event.pattern_match.group(1))
        name = event.pattern_match.group(2)

        chat = await event.get_chat()
        
        participants = await client.get_participants(chat)
        
        eligible_users = [p for p in participants if p.bot == False and not p.deleted]

        if len(eligible_users) < count:
            await event.reply(f"**Qrupta yetəri qədər istifadəçi mövcud deyil. Sadəcə {len(eligible_users)} istifadəçilər əlavə olunabilər**")
            return

        
        selected_users = random.sample(eligible_users, count)
        
        for user in selected_users:
            try:
                await client(functions.contacts.AddContactRequest(
                    id=user.id,
                    first_name=name,
                    last_name='',
                    phone='',
                    add_phone_privacy_exception=False
                ))
                await asyncio.sleep(1)  # İşlem yoğunluğunu azaltmak için kısa bir bekleme
            except Exception as e:
                print(f"Bir hata oluştu: {e}")

        await event.reply(f'{len(selected_users)} **İstifadəçilər uğurla kontakta əlavə olundu və {name} ilə dəyişdirildi 🎉**')

    except Exception as e:
        await event.reply(f'Xəta: {e}')

# qrup sifirla

@client.on(events.NewMessage(pattern="^.allban$", outgoing=True))
async def banall(event):
    if not is_owner(event):
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await event.edit("Bu əmri icra etmək üçün admin olmalısınız.")
        return

    await event.edit("Bütün istifadəçilər banlanır...")

    me = await event.client.get_me()
    all_participants = await event.client.get_participants(event.chat_id)
    for user in all_participants:
        if user.id == me.id:
            continue
        try:
            await event.client(EditBannedRequest(
                event.chat_id, user.id, ChatBannedRights(
                    until_date=None,
                    view_messages=True
                )
            ))
            await asyncio.sleep(0.5)
        except Exception as e:
            await event.reply(str(e))
        await asyncio.sleep(0.3)

    await event.edit("**༒ℍİ𝕂𝕆༒ girdi çıxdı😈**\n Qrup sıfırlandı")


# sozu terse cevir

@client.on(events.NewMessage(pattern= r'\.sback\s*(.*)'))
async def reverse_words(event):
    try:
        message = event.pattern_match.group(1)
        if event.is_reply and not message:
            reply_message = await event.get_reply_message()
            message = reply_message.message

        if message:
            ters_metn = ' '.join([kelme[::-1] for kelme in message.split()[::-1]])
            await event.edit(f"🔄 **Çevrilmiş cümlə:** {ters_metn}")
        else:
            await event.edit("🚫 **mətn daxil edilməyib**")
    
    except Exception as e:
        await event.reply(f"**Xeta:** {str(e)}")

# profil kolaj

@client.on(events.NewMessage(pattern=r'\.profilkolaj\s+(@\w+(?:\s+@\w+)*)'))
async def profile_pic_collage(event):
    try:

        usernames = event.pattern_match.group(1).split()

        if not os.path.exists("profile_pics"):
            os.makedirs("profile_pics")

        profile_pics = []
        for username in usernames:
            user = await client.get_entity(username)
            if user.photo:
                photos = await client(functions.photos.GetUserPhotosRequest(
                    user_id = user.id,
                    offset = 0,
                    max_id = 0,
                    limit = 1
                ))
                if photos.photos:
                    photo = photos.photos[0]
                    file = await client.download_media(photo, file="profile_pics/")
                    profile_pics.append(file)

        images = [Image.open(pic) for pic in profile_pics]
        widths,heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        collage = Image.new('RGB', (total_width,max_height))

        x_offset = 0
        for img in images:
            collage.paste(img, (x_offset,0))
            x_offset += img.width

        collage_file = "collage.jpg"
        collage.save(collage_file)
        
        await client.send_file(event.chat_id, collage_file, caption = "**Istifadəçilərin profilləri birləşdirildi**")
        
        for pic in profile_pics:
            os.remove(pic)
        os.remove(collage_file)

    except Exception as e:
        await event.reply(f"Xeta: {str(e)}")

# stats komutu 

@client.on(events.NewMessage(pattern=r'\.bansayi'))
async def allbanuser(event):
    try:
        # Qrup ID'sini alın
        chat = await event.get_input_chat()

        banned_users = await client.get_participants(chat, filter=ChannelParticipantsKicked)
        total_bans = len(banned_users)

        fban_users = await client.get_participants(chat, filter=ChannelParticipantsBanned)
        total_fbans = len(fban_users)

        stats_message = (
            f"🚫 **Banlı istifadəçilər:** `{total_bans}`\n"
            f"🔨 **Fbanlı istifadəçilər:** `{total_fbans}`"
        )
        await event.reply(stats_message)

    except Exception as e:
        await event.reply(f"🚫 Xəta baş verdi: {str(e)}")

# cihaz prosessor yoxlanisi

@client.on(events.NewMessage(pattern=r'\.prosessor'))
async def processor(event):
    try:

        await event.delete()

        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq().current

        report = (
            f"🖥 **Processor report**:\n\n"
            f"🔍 **Usage Percentage:** `{cpu_percent}%`\n"
            f"⚙️ **Number of Cores:** `{cpu_count}`\n"
            f"📊 **Frequency:** `{cpu_freq} MHZ`\n"
        )

        await event.reply(report)

    except Exception as e:
        await event.reply(f"🚫 Xəta baş verdi: {str(e)}")

# istifadəci informasiyasi

user_data = {}

# Kullanıcı verilerini JSON dosyasına kaydetmek için fonksiyon
def save_user_data():
    with open("user_data.json", "w") as f:
        json.dump(user_data, f, indent=4)

# Kullanıcı verilerini yüklemek için fonksiyon
def load_user_data():
    global user_data
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}

load_user_data()

# .usinfo komutu ile kullanıcının bilgilerini gösteren fonksiyon
@client.on(events.NewMessage(pattern=r"\.info"))
async def user_info(event):
    user = None
    message = event.message

    if message.is_reply:
        user = await message.get_reply_message()
        user = user.sender
    else:
        args = event.message.text.split()
        if len(args) < 2:
            await event.reply("İstifadə: .usinfo <istifadəçi_id | istifadəçi_tag> və ya bir istifadəçi mesajına cavab verərək .usinfo yazın")
            return

        identifier = args[1]

        try:
            if identifier.isdigit():
                user = await client.get_entity(int(identifier))
            else:
                user = await client.get_entity(identifier)
        except Exception as e:
            await event.reply(f"Xəta baş verdi: {str(e)}")
            return

    if user:
        user_id = str(user.id)
        first_name = user.first_name

        if user_id not in user_data:
            user_data[user_id] = {"first_names": []}

        if first_name not in user_data[user_id]["first_names"]:
            user_data[user_id]["first_names"].append(first_name)
            save_user_data()

        first_names_list = '\n'.join(user_data[user_id]["first_names"])

        user_details = (
            f"**İstifadəçi Məlumatı**\n"
            f"ID: {user.id}\n"
            f"Adı: {user.first_name}\n"
            f"Soyadı: {user.last_name}\n"
            f"İstifadəçi Adı: @{user.username}\n"
            f"Telefon Nömrəsi: {user.phone}\n"
            f"Botdur: {user.bot}\n"
            f"Dil Kodu: {user.lang_code}\n"
            f"\n**İstifadə etdiyi Adlar:**\n{first_names_list}"
        )
        await event.reply(user_details)
    else:
        await event.reply("İstifadəçi tapılmadı.")

@client.on(events.NewMessage())
async def track_first_names(event):
    user = event.sender
    if user:
        user_id = str(user.id)
        first_name = user.first_name

        if user_id not in user_data:
            user_data[user_id] = {"first_names": []}

        if first_name not in user_data[user_id]["first_names"]:
            user_data[user_id]["first_names"].append(first_name)
            save_user_data()

# fikir toplusu

brainstorm_ideas = {}

@client.on(events.NewMessage(pattern=r"\.ideya (.+)$"))
async def fikir(event):
    if not event.is_group:
        await event.reply("**Bu əmri yalnız qruplarda istifadə edə bilərsiniz**")
        return

    topic = event.pattern_match.group(1)
    chat_id = event.chat_id

    if chat_id not in brainstorm_ideas:
        brainstorm_ideas[chat_id] = {"topic": topic, "ideas": []}
        await event.reply(f"**'{topic}' mövzusunda beyin fırtınası başladı! Fikirlərinizi yazın:**")
    else:
        await event.reply(f"**Artıq '{brainstorm_ideas[chat_id]['topic']}' mövzusunda beyin fırtınası davam edir. Fikirlərinizi yazın:**")

@client.on(events.NewMessage)
async def collect_ideas(event):
    chat_id = event.chat_id

    if chat_id in brainstorm_ideas and event.message.text and not event.message.text.startswith('.'):
        idea = event.message.text
        brainstorm_ideas[chat_id]["ideas"].append(idea)

# movzu haqqinda fikirler

@client.on(events.NewMessage(pattern=r"\.ideyalar$"))
async def show_ideas(event):
    if not event.is_group:
        await event.reply("**Bu əmri yalnız qruplarda istifadə edə bilərsiniz**")
        return

    chat_id = event.chat_id

    if chat_id in brainstorm_ideas:
        ideas = brainstorm_ideas[chat_id]["ideas"]
        if ideas:
            ideas_text = "\n".join(f"- {idea}" for idea in ideas)
            await event.reply(f"**'{brainstorm_ideas[chat_id]['topic']}' mövzusunda toplanan fikirlər:**\n{ideas_text}")
        else:
            await event.reply("**Hələ heç bir fikir toplanmayıb**")
    else:
        await event.reply("**Hazırda davam edən bir beyin fırtınası yoxdur**")

@client.on(events.NewMessage(pattern=r"\.stopideya$"))
async def end_brainstorm(event):
    if not event.is_group:
        await event.reply("**Bu əmri yalnız qruplarda istifadə edə bilərsiniz**")
        return

    chat_id = event.chat_id

    if chat_id in brainstorm_ideas:
        del brainstorm_ideas[chat_id]
        await event.reply("**Beyin fırtınası bitdi! Toplanan fikirlərə baxmaq üçün `.fikirlər` yazın**")
    else:
        await event.reply("**Bitirilecek bir beyin fırtınası yoxdur**")


@client.on(events.NewMessage(pattern=r'\.songorulme\s+(@\S+)'))
async def lastseen(event):
    try:
        username = event.pattern_match.group(1)
        user = await client.get_entity(username)

        # Azərbaycan saat zonası
        az_time_zone = pytz.timezone('Asia/Baku')

        if user.status:
            if isinstance(user.status, UserStatusOnline):
                await event.edit(f"**{username} indi online-dir**")
            elif isinstance(user.status, UserStatusOffline):
                # Tarixi Azərbaycan vaxtına çevir
                last_seen = user.status.was_online.astimezone(az_time_zone).strftime("%d-%m-%Y %H:%M:%S")
                await event.edit(f"**{username} sonuncu dəfə {last_seen} tarixində online olub**")
            elif isinstance(user.status, UserStatusRecently):
                await event.edit(f"**{username} son vaxtlar online olub**")
            elif isinstance(user.status, UserStatusLastWeek):
                await event.edit(f"**{username} keçən həftə online olub**")
            elif isinstance(user.status, UserStatusLastMonth):
                await event.edit(f"**{username} keçən ay online olub**")
            else:
                await event.edit(f"**{username} çox uzun müddətdir online deyil**")
        else:
            await event.edit(f"**{username}'in online vəziyyəti mövcud deyil**")

    except Exception as e:
        await event.edit(f"**Xeta: {str(e)}**")

SOUNDS_DIR = "sounds/"

# .sounds komutu
@client.on(events.NewMessage(pattern=r"\.sounds$"))
async def list_sounds(event):
    if not is_owner(event):
        return
    
    try:
        sound_files = os.listdir(SOUNDS_DIR)
        sound_list = "\n".join(f"→ {os.path.splitext(file)[0]}" for file in sound_files)
        
        if sound_list:
            await event.edit(f"**Mövcud səs faylları:**\n\n{sound_list}")
        else:
            await event.reply("**Heç bir səs faylı tapılmadı**")

    except Exception as e:
        await event.reply(f"**Bir xəta baş verdi:** {str(e)}")

SOUNDS_DIR = "sounds/"

# $ komutu
@client.on(events.NewMessage(pattern=r"\$([^\s]+)$"))
async def send_sound(event):
    if not is_owner(event):
        return

    sound_name = event.pattern_match.group(1).strip()
    
    try:
        sound_file = os.path.join(SOUNDS_DIR, f"{sound_name}.mp3")
        
        if os.path.exists(sound_file):
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                await client.send_file(event.chat_id, sound_file, caption=f"**ᴄᴏʟᴅ sᴏᴜɴᴅ ᴇғғᴇᴄᴛ**", reply_to=reply_msg.id)
            else:
                await client.send_file(event.chat_id, sound_file, caption=f"**ᴄᴏʟᴅ sᴏᴜɴᴅ ᴇғғᴇᴄᴛ**")
            
            # Komutu içeren mesajı sil
            await event.delete()
        else:
            await event.reply("**Göstərilən adla bir səs faylı tapılmadı**")

    except Exception as e:
        await event.reply(f"**Bir xəta baş verdi:** {str(e)}")


SOUNDS_DIR = "sounds/"

# .addsound komutu
@client.on(events.NewMessage(pattern=r"\.add\s+(\S+)$"))
async def add_sound(event):
    if not is_owner(event):
        return

    sound_name = event.pattern_match.group(1).strip()
    
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        
        if reply_msg.voice or reply_msg.audio:
            try:
                # Ses dosyasını indir
                file_path = await client.download_media(reply_msg, file=SOUNDS_DIR)
                
                # MP3 formatına dönüştür
                audio = AudioSegment.from_file(file_path)
                output_file = os.path.join(SOUNDS_DIR, f"{sound_name}.mp3")
                
                audio.export(output_file, format="mp3")
                
                await event.edit(f"**{sound_name}** 𝚜ə𝚜 𝚜𝚘𝚞𝚗𝚍 𝚏𝚊𝚢𝚕ı𝚗𝚊 ə𝚕𝚊𝚟ə 𝚎𝚍𝚒𝚕𝚍𝚒")
                
            except Exception as e:
                if "ffmpeg" in str(e).lower():
                    await event.reply("❌ Xəta baş verdi: FFmpeg ile ilgili bir problem oluştu.")
                else:
                    await event.reply(f"❌ Xəta baş verdi: {str(e)}")
        else:
            await event.reply("**Reply atdığınız mesaj bir səs mesajı deyil**")
    else:
        await event.reply("**Bu əmri bir səs mesajına reply edərək istifadə edin**")

# istifadeci informasiya

user_data = {}

# Kullanıcı verilerini JSON dosyasına kaydetmek için fonksiyon
def save_user_data():
    with open("user_data.json", "w") as f:
        json.dump(user_data, f, indent=4)

# Kullanıcı verilerini yüklemek için fonksiyon
def load_user_data():
    global user_data
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}

load_user_data()

# .usinfo komutu ile kullanıcının bilgilerini gösteren fonksiyon
@client.on(events.NewMessage(pattern=r"\.usinfo"))
async def user_info(event):
    if not is_owner(event):
        return
    user = None
    message = event.message

    if message.is_reply:
        user = await message.get_reply_message()
        user = user.sender
    else:
        args = event.message.text.split()
        if len(args) < 2:
            await event.edit("İstifadə: .usinfo <istifadəçi_id | istifadəçi_tag> və ya bir istifadəçi mesajına cavab verərək .usinfo yazın")
            return

        identifier = args[1]

        try:
            if identifier.isdigit():
                user = await client.get_entity(int(identifier))
            else:
                user = await client.get_entity(identifier)
        except Exception as e:
            await event.reply(f"Xəta baş verdi: {str(e)}")
            return

    if user:
        user_id = str(user.id)
        first_name = user.first_name

        if user_id not in user_data:
            user_data[user_id] = {"first_names": []}

        if first_name not in user_data[user_id]["first_names"]:
            user_data[user_id]["first_names"].append(first_name)
            save_user_data()

        first_names_list = '\n'.join(user_data[user_id]["first_names"])

        user_details = (
            f"ℹ️ 𝚄𝚜𝚎𝚛 𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗\n\n"
            f"`ID`: {user.id}\n"
            f"`Adı`: {user.first_name}\n"
            f"`Soyadı`: {user.last_name}\n"
            f"`İstifadəçi Adı`: @{user.username}\n"
            f"`Telefon Nömrəsi`: {user.phone}\n"
            f"`Botdur`: {user.bot}\n"
            f"`Dil Kodu`: {user.lang_code}\n\n"
            f"\n𝚃𝚑𝚎 𝙽𝚊𝚖𝚎𝚜 𝙷𝚎 𝚄𝚜𝚎𝚜:\n```{first_names_list}```"
        )
        await event.edit(user_details)
    else:
        await event.edit("İstifadəçi tapılmadı.")

@client.on(events.NewMessage())
async def track_first_names(event):
    user = event.sender
    if user:
        user_id = str(user.id)
        first_name = user.first_name

        if user_id not in user_data:
            user_data[user_id] = {"first_names": []}

        if first_name not in user_data[user_id]["first_names"]:
            user_data[user_id]["first_names"].append(first_name)
            save_user_data()

# klon komutu

original_profile = {}
original_photo_path = None

@client.on(events.NewMessage(pattern=r'^\.klon$', outgoing=True))
async def clone_profile(event):
    global original_photo_path
    reply = await event.get_reply_message()
    if not reply or not reply.sender_id:
        await event.edit("Zəhmət olmasa, bir istifadəçinin mesajına cavab verin.")
        return

    user_full = await client(GetFullUserRequest(reply.sender_id))
    user = user_full.users[0]
    if not user:
        await event.edit("`İstifadəçi tapılmadı`")
        return

    user_first_name = user.first_name or ""
    await event.edit(f"{user_first_name} `prifilini klonlayıram🙈...`")

    try:
        
        me_full = await client(GetFullUserRequest('me'))
        me = me_full.users[0]
        original_profile['first_name'] = me.first_name
        original_profile['last_name'] = me.last_name
        original_profile['bio'] = me_full.full_user.about if me_full.full_user.about else ''

      
        photos = await client.get_profile_photos('me')
        if photos:
            original_photo = photos[0]
            original_photo_path = await client.download_media(original_photo, file='original_photo.jpg')
        else:
            original_photo_path = None

        
        photos = await client.get_profile_photos(user)
        if photos:
            photo = photos[0]
            uploaded_photo_path = await client.download_media(photo, file='uploaded_photo.jpg')

            
            with open(uploaded_photo_path, 'rb') as f:
                uploaded_photo = await client.upload_file(f)
            await client(UploadProfilePhotoRequest(file=uploaded_photo))
        else:
            await event.edit("`Bu istifadəçinin profil şəkli yoxdur`")


        await client(UpdateProfileRequest(
            first_name=user.first_name,
            last_name=user.last_name,
            about=user_full.full_user.about if user_full.full_user.about else ''
        ))

        await event.reply("`Profil uğurla klonlandı`")
    except Exception as e:
        await event.edit(f"Bir xəta baş verdi: {str(e)}")
    
       

@client.on(events.NewMessage(pattern=r'^\.geri$', outgoing=True))
async def revert_profile(event):
    if not original_profile:
        await event.edit("`Klonlanmış profil məlumatları tapılmadı`")
        return

    try:
        await event.edit("`Orijinal profilə geri dönülür...`")

        
        if original_photo_path and os.path.exists(original_photo_path):
            with open(original_photo_path, 'rb') as f:
                original_photo = await client.upload_file(f)
            await client(UploadProfilePhotoRequest(file=original_photo))
            os.remove(original_photo_path)


        await client(UpdateProfileRequest(
            first_name=original_profile['first_name'],
            last_name=original_profile['last_name'],
            about=original_profile['bio']
        ))

        await event.reply("`Profil uğurla geri yükləndi`")
    except Exception as e:
        await event.edit(f"Bir xəta baş verdi: {str(e)}")

AZ_TIMEZONE = pytz.timezone('Asia/Baku')

async def update_name(client):
    while True:
        current_time = datetime.now(AZ_TIMEZONE).strftime("%H:%M")

        me = await client.get_me()
        first_name = me.first_name

        if len(first_name) + len(current_time) <= 64:
            new_last_name = current_time
        else:
            # Aksi takdirde saat kısmını kısaltıyoruz
            new_last_name = current_time[:64 - len(first_name)]

        await client(functions.account.UpdateProfileRequest(
            first_name=first_name,
            last_name=new_last_name
        ))

        await asyncio.sleep(60)

@client.on(events.NewMessage(pattern=r"\.tname$"))
async def tname(event):
    await event.edit("`Adınıza saat əlavə olundu`")

    await update_name(client)

# basqin komutu

spam_tasks = []

@client.on(events.NewMessage(pattern=r"\.ride (.+)"))
async def ride(event):
    if not is_owner(event):
        return
    message_to_spam = event.pattern_match.group(1)
    task = asyncio.create_task(spam_messages(event, message_to_spam))
    spam_tasks.append(task)
    await event.delete()

async def spam_messages(event, message):
    for i in range(100):
        await event.respond(message)
        await asyncio.sleep(1)
        if spam_tasks and any(task.cancelled() for task in spam_tasks):
            break

@client.on(events.NewMessage(pattern=r"\.stopride$"))
async def stopride(event):
    if not is_owner(event):
        return
    global spam_tasks

    if spam_tasks:
        for task in spam_tasks:
            task.cancel()

        await event.edit("`Bütün spam əməliyyatları dayandırıldı!`")
        spam_tasks = []
    else:
        await event.edit("`Davam edən spam əməliyyatı yoxdur`")


# filter

FILTERS_FILE = 'filters.json'

# Filtrleri yükleme
def load_filters():
    if os.path.exists(FILTERS_FILE):
        with open(FILTERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_filters(filters):
    with open(FILTERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(filters, f, ensure_ascii=False, indent=4)  # UTF-8 dəstəyi üçün

filters = load_filters()

@client.on(events.NewMessage(pattern=r'\.filter (.+)'))
async def add_filter(event):
    if not event.is_reply:
        await event.edit("`Bir mesaja cavab olaraq bu əmri istifadə edin!`")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg or not reply_msg.text:
        await event.edit("`Cavab verdiyin mesaj mətn deyil`")
        return

    keyword = reply_msg.text.strip().lower()  # Cavab verilmiş mesaj açar sözdür
    reply_text = event.pattern_match.group(1).strip()  # .filter-dən sonra yazılan mətn cavabdır

    if not reply_text:
        await event.edit("`Filtr təyin etmək üçün bir cavab mətni yaz`")
        return

    filters[keyword] = reply_text
    save_filters(filters)

    await event.edit(f"`{keyword}` **açar sözü üçün filtr təyin edildi!\nCavab:** `{reply_text}`")

@client.on(events.NewMessage(pattern=r'\.filtersil (.+)'))
async def remove_filter(event):
    keyword = event.pattern_match.group(1).strip().lower()
    if keyword in filters:
        del filters[keyword]
        save_filters(filters)
        await event.edit(f"`{keyword}` **açar sözü üçün filtr silindi**")
    else:
        await event.edit(f"`{keyword}` **filter tapılmadı**")

@client.on(events.NewMessage(pattern=r'\.filters'))
async def list_all_filters(event):
    if not filters:
        await event.edit("`Hal-hazırda heç bir filtr təyin edilməyib`")
        return

    filter_list = "\n".join([f"`{keyword}`: `{reply}`" for keyword, reply in filters.items()])
    await event.edit(f"Filterlər:\n\n{filter_list}")

@client.on(events.NewMessage(pattern=r'\.delfilterall'))
async def delete_all_filters(event):
    if not filters:
        await event.edit("`Silinəcək heç bir filtr yoxdur`")
        return

    last_filter = list(filters.items())[-1]
    filters.clear()
    filters[last_filter[0]] = last_filter[1]

    save_filters(filters)

    await event.edit(f"`Bütün filtrlər silindi`")

@client.on(events.NewMessage)
async def auto_reply(event):
    message_text = event.raw_text.strip().lower()

    for keyword, reply_text in filters.items():
        if message_text == keyword: 
            await event.reply(reply_text) 
            break

print("bot aktivdir")
client.start()
client.run_until_disconnected()