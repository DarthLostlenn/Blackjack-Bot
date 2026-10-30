import discord
import os
import json
from discord import app_commands; import random
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree (client)
@tree.command(name="ping", description="Antwortet mit Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@client.event
async def on_ready():
    await tree.sync()
    print('Bot ist Online!')

token = os.getenv("TOKEN")

@tree.command(name="muenzwurf", description= "Wirft eine Münze und zeigt das Ergebnis an.")
async def muenzwurf(interaction: discord.Interaction):
    if interaction.channel.name != "gamba":
        await interaction.response.send_message("Dieser Befehl kann nur im #gamba-Kanal verwendet werden.", ephemeral=True)
        return
    ergebnis = random.choice(["Kopf", "Zahl"])
    await interaction.response.send_message(f"Die Münze zeigt: {ergebnis}")

class Testview(discord.ui.View):
    @discord.ui.button(label="Klick mich!", style=discord.ButtonStyle.primary)
    async def klick(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Du hast den Button geklickt!", ephemeral=True)

@tree.command(name="testbutton", description="Testet den Button.")
async def testbutton(interaction: discord.Interaction):
    await interaction.response.send_message("Das ist ein Testbutton:", view=Testview())

import blackjack

class BlackjackView(discord.ui.View):
    def __init__(self, deck, spieler_hand, dealer_hand):
        super().__init__()
        self.deck = deck
        self.spieler_hand = spieler_hand
        self.dealer_hand = dealer_hand
    @discord.ui.button(label="Hit!", style=discord.ButtonStyle.success)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        karte = self.deck.pop()
        self.spieler_hand.append(karte)
        neue_punkte = blackjack.hand_wert(self.spieler_hand)
        if neue_punkte > 21:
            await interaction.message.edit(content=f"Bust!{self.spieler_hand} sind {neue_punkte} Punkte. Dealer gewinnt!", view=None)
        else:
            await interaction.message.edit(content=f"Spielerhand: {self.spieler_hand} Punkte: {neue_punkte}\nDealerhand: {self.dealer_hand} Punkte: {blackjack.hand_wert(self.dealer_hand)}", view=self)
    @discord.ui.button(label="Stand!", style=discord.ButtonStyle.danger)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        while blackjack.hand_wert(self.dealer_hand) < 17:
            karte = self.deck.pop()
            self.dealer_hand.append(karte)
        dealer_punkte = blackjack.hand_wert(self.dealer_hand)
        spieler_punkte = blackjack.hand_wert(self.spieler_hand)
        if dealer_punkte > 21:
            ergebnis = "Dealer hat überkauft! Du gewinnst."
        elif spieler_punkte > dealer_punkte:
            ergebnis = "Du gewinnst!"
        elif spieler_punkte < dealer_punkte:
            ergebnis = "Dealer gewinnt!"
        else:
            ergebnis = "Unentschieden!"
        await interaction.message.edit(content=f"Spieler: {spieler_punkte} | Dealer: {dealer_punkte}\n{ergebnis}", view=None)

@tree.command(name="blackjack", description="Startet ein neues Blackjack-Spiel.")
async def blackjack_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    coins = get_user_coins(user_id)
    if coins < 10:
        await interaction.response.send_message("Du hast nicht genug Münzen, um Blackjack zu spielen. Du benötigst mindestens 10 Münzen.", ephemeral=True)
        return
    change_coins(user_id, -10)
    farben = ["Herz", "Karo", "Kreuz", "Pik"]
    werte = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]
    deck = []
    for farbe in farben:
        for wert in werte:
            deck.append(farbe + " " + wert)
    random.shuffle(deck)
    spieler_hand = []
    dealer_hand = []
    karte = deck.pop()
    spieler_hand.append(karte)
    karte = deck.pop()
    spieler_hand.append(karte)
    karte = deck.pop()
    dealer_hand.append(karte)
    karte = deck.pop()
    dealer_hand.append(karte)
    await interaction.response.send_message(f"Spielerhand: {spieler_hand} Punkte: {blackjack.hand_wert(spieler_hand)})\nDealerhand: {dealer_hand} Punkte: {blackjack.hand_wert(dealer_hand)})", view=BlackjackView(deck, spieler_hand, dealer_hand))




DATEI = "coins.json"
def get_user_coins(user_id):
    try:
        with open(DATEI,"r") as datei:
            alle_coins = json.load(datei)
    except FileNotFoundError:
        alle_coins = {}
    if user_id not in alle_coins:
        alle_coins[user_id] = 100
        save_coins(alle_coins)
    return alle_coins[user_id]

@tree.command(name="my_coins", description="Zeigt die Anzahl der Münzen an, die du hast.")
async def my_coins(interaction: discord.Interaction):
    if interaction.channel.name != "gamba":
        await interaction.response.send_message("Dieser Befehl kann nur im #gamba-Kanal verwendet werden.", ephemeral=True)
        return
    user_id = str(interaction.user.id)
    coins = get_user_coins(user_id)
    await interaction.response.send_message(f"{interaction.user.mention}, du hast {coins} Münzen.")

def save_coins(alle_coins):
    with open(DATEI, "w") as datei:
        json.dump(alle_coins, datei)

def change_coins(user_id, betrag):
    with open(DATEI, "r") as datei:
        alle_coins = json.load(datei)
        alle_coins[user_id] += betrag
    with open(DATEI, "w") as datei:
        json.dump(alle_coins, datei)
client.run(token)