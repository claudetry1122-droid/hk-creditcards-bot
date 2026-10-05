# HK Credit Card Bot 🇭🇰

A Telegram bot that recommends the best credit card for every purchase category based on your own wallet.

---

## Setup

### 1. Get your Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Pick a name (e.g. `My HK Cards Bot`) and a username ending in `bot` (e.g. `myhkcards_bot`)
4. BotFather will give you a token like `1234567890:ABC-DEF...` — copy it

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your token

```bash
cp .env.example .env
```

Edit `.env` and replace `your_telegram_bot_token_here` with the token from BotFather.

### 4. Run the bot

```bash
python bot.py
```

The bot runs locally. Keep this terminal window open while using it. Anyone can find and use the bot by its username on Telegram.

---

## Commands

| Command | Description |
|---|---|
| `/start` | Open the main menu |
| `/addcard` | Add one of your HK credit cards |
| `/mycards` | View & remove cards in your wallet |
| `/recommend` | Get the best card for a spending category |

---

## Cards in the database (19 cards, 8 banks)

| Bank | Cards |
|---|---|
| HSBC | Red, Visa Signature (RewardCash), EveryMile |
| Hang Seng | yuu Mastercard, MMPOWER World Mastercard |
| Citi | Cash Back, Rewards, PremierMiles |
| Standard Chartered | Smart, Cathay Mastercard, Simply Cash |
| sim | Credit Card, World Mastercard® |
| DBS | Black World Mastercard |
| BOC (Bank of China) | Chill |
| Digital Banks | Mox Credit, ZA Card |

To add more cards, edit `cards_data.py` — add an entry to `CARDS` and add the key to the relevant bank in `BANKS`.

---

## Notes

- Each user's card list is stored per-Telegram-user-ID in a local SQLite file (`cards_bot.db`)
- Reward rates are approximate and change frequently — always verify with the issuing bank
- The bot shows separate recommendations for cashback, miles, and points cards so you can choose based on your preference
- All card data was verified against official bank websites (Oct 2024)
