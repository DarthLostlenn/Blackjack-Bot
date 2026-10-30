import random
farben = ["Herz", "Karo", "Kreuz", "Pik"]
werte = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]
deck = []
for farbe in farben:
    for wert in werte:
        (deck.append(farbe + " " + wert))
random.shuffle(deck)
random.choice(deck)
print("Verbleibende Karten:" + str(len(deck)))
#wenn Bube, Dame, König gezogen wird-> Wert 10 und wenn eine 2-10 gezogen wird, ist der Wert die Zahl selbst. Wenn ein Ass gezogen wird-> entweder 1 oder 11.
def karten_wert(karte):
    if "Bube" in karte or "Dame" in karte or "König" in karte:
        return 10
    elif "Ass" in karte:
        return 11  
    else:
        return int(karte.split()[1])  

def hand_wert(hand):
    punkte = 0
    for karte in hand:
        punkte += karten_wert(karte)
    return punkte 

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

print(f"Spielerhand: {spieler_hand} Punkte: {hand_wert(spieler_hand)}")
print(f"Dealerhand: {dealer_hand} Punkte: {hand_wert(dealer_hand)}")

antwort = input("Möchtest du eine weitere Karte ziehen? (j/n): ")
while antwort.lower() == "j":
    karte = deck.pop()
    spieler_hand.append(karte)
    print(f"Spielerhand: {spieler_hand} Punkte: {hand_wert(spieler_hand)}")
    if hand_wert(spieler_hand) > 21:
        print("Du hast überkauft! Dealer gewinnt.")
        break
    antwort = input("Möchtest du eine weitere Karte ziehen? (j/n): ")

if hand_wert(spieler_hand) <= 21:
    while hand_wert(dealer_hand) < 17:
        karte = deck.pop()
        dealer_hand.append(karte)
        print(f"Dealerhand: {dealer_hand} Punkte: {hand_wert(dealer_hand)}")
    if hand_wert(dealer_hand) > 21:
        print("Dealer hat überkauft! Du gewinnst.")
    elif hand_wert(spieler_hand) > hand_wert(dealer_hand):
        print("Du gewinnst!")
    elif hand_wert(spieler_hand) < hand_wert(dealer_hand):
        print("Dealer gewinnt!")
    else:
        print("Unentschieden!")

