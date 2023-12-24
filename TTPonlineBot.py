from os import name
import discord
from mcstatus import JavaServer
from discord.ext import commands

# Устанавливаем интенты для работы с сообщениями
intents = discord.Intents.default()
intents.messages = True
intents.guild_messages = True
intents.message_content = True
ttp = JavaServer.lookup("ttp.su:25565")

# Функция для чтения токена из файла
def read_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()  # Считываем токен и удаляем возможные пробелы или символы переноса строки
token = read_token()

bot = commands.Bot(command_prefix='!', intents=intents) # Создаем экземпляр бота с префиксом '!'
# Событие, которое срабатывает при успешном подключении бота к Discord
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("TimeToPlay"))
    print(f'{bot.user} готов к работе')


@bot.command(name='лист_ттп')
async def _list(lists):
    ttp_query = ttp.query()
    ttp_status = ttp.status()
    
    players = ttp_query.players.names
    
    # Заменяем символы "_" и "-" в именах игроков
    sanitized_players = [player.replace('_', r'\_').replace('-', r'\-') for player in players]

    # Создаем словарь для категорий
    categories = {
        "**[ᴅᴇᴠᴇʟᴏᴘᴇʀ]:**": ["Snele", "morols", "sovich228"],

        "**[ꜱᴛᴀꜰꜰ]:**": [".melo4ek", "Melo4ek", "TheCatSwears", "asyawarrior"],

        "**[sᴛ.ᴍᴏᴅᴇʀ]:**": ["xx\\_uuiovv", "\\_mentosis\\_", " MasecroEX"],

        "**[ᴍᴏᴅᴇʀᴀᴛᴏʀ]:**": ["TOBI\\_RAY", "\\_Sarquz", "\\_Xlebysheck\\_", "BeFos", "Artem0"],

        "**[ʜᴇʟᴘᴇʀ]:**": ["josmack", "kaaprka", "Schalke"],

        "**[ʙᴜɪʟᴅᴇʀ]:**": ["derov1ch", "serhtru", ".mnk", "folin01"]
    }

    # Создаем список для игроков, не принадлежащих к какой-либо категории
    uncategorized_players = []
    
    # Перебираем игроков и распределяем их по категориям
    categorized_players = {}
    for player, sanitized_player in zip(players, sanitized_players):
        added_to_category = False
        for category, category_players in categories.items():
            if sanitized_player in category_players:
                categorized_players.setdefault(category, []).append(sanitized_player)
                added_to_category = True
                break
        if not added_to_category:
            uncategorized_players.append(sanitized_player)
    
    # Формируем сообщение с категориями и игроками
    message = "На сервере \"TimeToPlay\":\n \n"
    
    # Добавляем игроков из категорий
    for category, category_players in categorized_players.items():
        message += f"{category} {', '.join(category_players)}\n\n"  # Добавляем пустую строку после каждой категории
    
    # Добавляем игроков без категории
    if uncategorized_players:
        message += "**Без категории (Игроки):** " + ', '.join(uncategorized_players) + "\n"
    

    all_player = ttp_status.players.online / 2
    message += f"\nВсего игроков: {all_player}"

    in_embed = discord.Embed( # Создаем эмбед для сообщения внутри тикета
            title="Список людей TTP",
            description=message,
            color=0xD69E6D
        )
    in_embed.set_author(name="Автор бота: Imrasts")
    view = discord.ui.View()
    await lists.reply(embed=in_embed, view=view, ephemeral=True)

# Запускаем бота
bot.run(token)
