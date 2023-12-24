import discord
from mcstatus import JavaServer
from discord.ext import commands
from collections import OrderedDict

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

bot = commands.Bot(command_prefix='!', intents=intents)  # Создаем экземпляр бота с префиксом '!'

# Событие, которое срабатывает при успешном подключении бота к Discord
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("TimeToPlay"))
    print(f'{bot.user} готов к работе')

# Упорядоченный словарь для категорий и игроков
categories = OrderedDict([
    ("**[ᴅᴇᴠᴇʟᴏᴘᴇʀ]:**", ["Snele", "morols", "sovich228"]),
    ("**[ꜱᴛᴀꜰꜰ]:**", [".melo4ek", "Melo4ek", "TheCatSwears", "asyawarrior"]),
    ("**[sᴛ.ᴍᴏᴅᴇʀ]:**", ["xx\\_uuiovv", "\\_mentosis\\_", " MasecroEX"]),
    ("**[ᴍᴏᴅᴇʀᴀᴛᴏʀ]:**", ["TOBI\\_RAY", "\\_Sarquz", "\\_Xlebysheck\\_", "BeFos", "Artem0"]),
    ("**[ʜᴇʟᴘᴇʀ]:**", ["josmack", "kaaprka", "Schalke"]),
    ("**[ʙᴜɪʟᴅᴇʀ]:**", ["derov1ch", "serhtru", ".mnk", "folin01", "Mr\\_\\_Mechanic"])
])

# Команда для вывода списка игроков на сервере
@bot.command(name='лист_ттп', aliases=["Лист_ттп", "Лист_ТТП", "Лист_Ттп", "лист_ТТП", "ЛИСТ_ТТП", "лист_Ттп"])
async def _list(lists):
    # Получаем информацию о сервере
    ttp_query = ttp.query()
    ttp_status = ttp.status()
    
    # Получаем список игроков и их "очищенные" версии
    players = ttp_query.players.names
    sanitized_players = [player.replace('_', r'\_').replace('-', r'\-') for player in players]

    # Упорядоченный словарь для категорий и игроков
    categorized_players = OrderedDict((category, []) for category in categories)
    uncategorized_players = []
    
    # Распределяем игроков по категориям
    for player, sanitized_player in zip(players, sanitized_players):
        added_to_category = False
        for category, category_players in categories.items():
            if sanitized_player in category_players:
                categorized_players[category].append(sanitized_player)
                added_to_category = True
                break
        if not added_to_category:
            uncategorized_players.append(sanitized_player)
    
    # Формируем сообщение с категориями и игроками
    message = "На сервере \"TimeToPlay\":\n \n"
    
    # Добавляем игроков из категорий
    for category, category_players in categorized_players.items():
        message += f"{category} {' **|** '.join(category_players)}\n\n"
    
    # Добавляем игроков без категории
    if uncategorized_players:
        message += "**Без категории (Игроки):** " + ' **|** '.join(uncategorized_players) + "\n"
    
    # Получаем общее количество игроков
    all_player = int(ttp_status.players.online / 2)
    message += f"\nВсего игроков: {all_player}"

    # Создаем эмбед для сообщения внутри тикета
    in_embed = discord.Embed(
        title="Список людей TTP:",
        description=message,
        color=0xD69E6D
    )
    in_embed.set_author(name="Автор бота: Imrasts")
    view = discord.ui.View()
    await lists.reply(embed=in_embed, view=view, ephemeral=True)

# Запускаем бота
bot.run(token)
