import discord, os, sqlite3, asyncio, random
from discord import app_commands

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DB_FILE = "delta_currency.db"
GACHA_ANIMATION_PATH = "free_gacha_animation.gif"
GACHA_COST = 10
CURRENCY_UNIT = "デルタ"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS currency (user_id TEXT PRIMARY KEY, balance INTEGER NOT NULL)")
    conn.close()
def get_balance(uid):
    conn = sqlite3.connect(DB_FILE)
    r = conn.execute("SELECT balance FROM currency WHERE user_id = ?", (uid,)).fetchone()
    conn.close()
    return r[0] if r else 0
def add_balance(uid, amt):
    conn = sqlite3.connect(DB_FILE)
    n = get_balance(uid) + amt
    conn.execute("INSERT OR REPLACE INTO currency (user_id, balance) VALUES (?, ?)", (uid, n))
    conn.commit(); conn.close(); return n
def sub_balance(uid, amt):
    conn = sqlite3.connect(DB_FILE); n = max(0, get_balance(uid)-amt)
    conn.execute("UPDATE currency SET balance = ? WHERE user_id = ?", (n, uid)); conn.commit(); conn.close(); return n

class Bot(discord.Client):
    def __init__(self): super().__init__(intents=discord.Intents.default()); self.tree = app_commands.CommandTree(self)
    async def setup_hook(self): await self.tree.sync()
init_db(); bot = Bot()

@bot.tree.command(name="ガチャ", description=f"{GACHA_COST}{CURRENCY_UNIT}消費してガチャ")
async def gacha(interaction: discord.Interaction):
    uid = str(interaction.user.id); bal = get_balance(uid)
    if bal < GACHA_COST:
        await interaction.response.send_message(f"残高不足！（{bal}{CURRENCY_UNIT}）", ephemeral=True); return
    sub_balance(uid, GACHA_COST); nb = get_balance(uid)
    await interaction.response.defer(); await asyncio.sleep(0.5)
    await interaction.followup.send("ガチャを回します…")
    await asyncio.sleep(1)
    if os.path.exists(GACHA_ANIMATION_PATH):
        await interaction.followup.send(file=discord.File(GACHA_ANIMATION_PATH))
    else:
        await interaction.followup.send("演出画像なし")
    await asyncio.sleep(2)
    result = random.randint(1, 100)
    await interaction.followup.send(f"✨結果: {result}！残高: {nb}{CURRENCY_UNIT}")

@bot.tree.command(name="残高", description="自分の残高確認")
async def balance(interaction: discord.Interaction):
    bal = get_balance(str(interaction.user.id))
    await interaction.response.send_message(f"{interaction.user.mention} 残高: {bal}{CURRENCY_UNIT}")

if __name__ == "__main__":
    if TOKEN is None: print("DISCORD_BOT_TOKEN未設定")
    else: bot.run(TOKEN)