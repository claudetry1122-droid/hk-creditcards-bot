"""
HK Credit Card Recommendation Bot
Run: python bot.py
"""
import os
import logging

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

import database as db
from cards_data import BANKS, CARDS, CATEGORIES

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ── Reward lookup with parent-category fallback ───────────────────────────────

def _get_reward(card: dict, category: str) -> dict:
    """Return reward dict for category, falling back to parent then general."""
    if category in card["rewards"]:
        return card["rewards"][category]
    parent = CATEGORIES[category].get("parent")
    if parent and parent in card["rewards"]:
        return card["rewards"][parent]
    return card["rewards"]["general"]


# ── Keyboard builders ─────────────────────────────────────────────────────────

def _main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕  Add a Card",          callback_data="menu:addcard")],
        [InlineKeyboardButton("💳  My Cards",            callback_data="menu:mycards")],
        [InlineKeyboardButton("💡  Get Recommendation",  callback_data="menu:recommend")],
        [InlineKeyboardButton("⚙️  Reward Preference",   callback_data="menu:pref")],
        [InlineKeyboardButton("❓  Help",                callback_data="menu:help")],
    ])


def _back_kb(target: str = "main"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️  Back", callback_data=f"back:{target}")]
    ])


# ── /start ────────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.init_db()
    name = update.effective_user.first_name
    text = (
        f"👋 Hi {name}!\n\n"
        "I help you pick the *best credit card* for every purchase in Hong Kong 🇭🇰\n\n"
        "• Add the HK credit cards you own\n"
        "• Tell me what you're spending on\n"
        "• I'll show the card that earns you the most!\n\n"
        "What would you like to do?"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=_main_menu_kb())


# ── Command shortcuts ─────────────────────────────────────────────────────────

async def cmd_addcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.init_db()
    await update.message.reply_text(
        "🏦 Select your card's bank:",
        reply_markup=_bank_list_kb(),
    )


async def cmd_mycards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.init_db()
    user_id = update.effective_user.id
    card_ids = db.get_user_cards(user_id)
    text, kb = _my_cards_content(card_ids)
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)


async def cmd_recommend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.init_db()
    user_id = update.effective_user.id
    card_ids = db.get_user_cards(user_id)
    if not card_ids:
        await update.message.reply_text(
            "📭 You haven't added any cards yet.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add a Card", callback_data="menu:addcard")]
            ]),
        )
        return
    await update.message.reply_text(
        "💡 *What are you spending on?*\n\nPick a category:",
        parse_mode="Markdown",
        reply_markup=_category_kb(),
    )


# ── Inline keyboard content builders ─────────────────────────────────────────

def _bank_list_kb() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(bank, callback_data=f"bank:{bank}")] for bank in BANKS]
    rows.append([InlineKeyboardButton("⬅️  Back", callback_data="back:main")])
    return InlineKeyboardMarkup(rows)


def _cards_for_bank_kb(bank_name: str) -> InlineKeyboardMarkup:
    rows = []
    for card_id in BANKS.get(bank_name, []):
        card = CARDS[card_id]
        type_icon = {"cashback": "💰", "miles": "✈️", "points": "⭐"}.get(card["reward_type"], "💳")
        rows.append([InlineKeyboardButton(
            f"{type_icon}  {card['name']}",
            callback_data=f"addcard:{card_id}",
        )])
    rows.append([InlineKeyboardButton("⬅️  Back to Banks", callback_data="back:banks")])
    return InlineKeyboardMarkup(rows)


def _my_cards_content(card_ids: list[str]) -> tuple[str, InlineKeyboardMarkup]:
    if not card_ids:
        text = "📭 You haven't added any cards yet."
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add a Card",  callback_data="menu:addcard")],
            [InlineKeyboardButton("⬅️ Main Menu",  callback_data="back:main")],
        ])
        return text, kb

    text = f"💳 *Your Cards* ({len(card_ids)} added)\n\nTap a card to remove it:\n"
    rows = []
    for card_id in card_ids:
        card = CARDS.get(card_id)
        if not card:
            continue
        type_icon = {"cashback": "💰", "miles": "✈️", "points": "⭐"}.get(card["reward_type"], "💳")
        rows.append([InlineKeyboardButton(
            f"🗑️  {type_icon} {card['name']}",
            callback_data=f"removecard:{card_id}",
        )])
    rows.append([InlineKeyboardButton("➕ Add More Cards", callback_data="menu:addcard")])
    rows.append([InlineKeyboardButton("⬅️ Main Menu",     callback_data="back:main")])
    return text, InlineKeyboardMarkup(rows)


def _category_kb() -> InlineKeyboardMarkup:
    # Ordered display: top-level first, then sub-categories grouped logically
    ordered = [
        # Dining
        "dining", "dining_fastfood", "dining_delivery",
        # Online / shopping
        "online", "online_fashion", "supermarket_hktvmall",
        # Supermarkets
        "supermarket", "supermarket_parknshop", "supermarket_health_beauty",
        # Transport
        "transport", "transport_mtr_bus",
        # Travel
        "travel", "travel_cathay", "travel_klook", "hotels",
        # Entertainment
        "entertainment", "entertainment_cinema", "entertainment_streaming",
        # Utilities
        "utilities", "utilities_telecom",
        # Overseas
        "overseas", "overseas_japan",
        # General
        "general",
    ]
    rows = []
    for i in range(0, len(ordered), 2):
        row = []
        for cat_id in ordered[i:i+2]:
            info = CATEGORIES[cat_id]
            label = info["label"]
            # Indent sub-categories slightly with a bullet
            if info.get("parent") is not None:
                label = f"↳ {info['emoji']} {label}"
            else:
                label = f"{info['emoji']} {label}"
            row.append(InlineKeyboardButton(label, callback_data=f"cat:{cat_id}"))
        rows.append(row)
    rows.append([InlineKeyboardButton("⬅️  Back", callback_data="back:main")])
    return InlineKeyboardMarkup(rows)


# ── Recommendation logic ──────────────────────────────────────────────────────

def _build_recommendation(user_id: int, category: str) -> tuple[str, InlineKeyboardMarkup]:
    card_ids = db.get_user_cards(user_id)
    cat_info = CATEGORIES[category]
    pref = db.get_reward_pref(user_id)

    buckets: dict[str, list[dict]] = {"cashback": [], "miles": [], "points": []}

    for card_id in card_ids:
        card = CARDS.get(card_id)
        if not card:
            continue
        reward = _get_reward(card, category)
        buckets[card["reward_type"]].append({
            "name":    card["name"],
            "bank":    card["bank"],
            "reward":  reward,
            "tip":     card["tip"],
            "card_id": card_id,
        })

    for group in buckets.values():
        group.sort(key=lambda x: x["reward"]["sort_key"], reverse=True)

    # Order buckets based on user preference
    if pref == "cashback":
        bucket_order = ["cashback", "miles", "points"]
    elif pref == "miles":
        bucket_order = ["miles", "points", "cashback"]
    else:
        bucket_order = ["cashback", "miles", "points"]

    pref_label = {"cashback": "💰 cashback", "miles": "✈️ miles/points"}.get(pref)

    lines = [f"{cat_info['emoji']} *{cat_info['label']} — Best Cards*\n"]
    if pref_label:
        lines.append(f"_Showing {pref_label} first (your preference)_\n")

    icons = {"cashback": "💰", "miles": "✈️", "points": "⭐"}
    titles = {"cashback": "Best Cashback", "miles": "Best Miles", "points": "Best Points"}
    first_bucket = True

    for btype in bucket_order:
        group = buckets[btype]
        if not group:
            continue
        best = group[0]
        marker = " 👈 _Best for you_" if (first_bucket and pref != "all") else ""
        lines.append(f"{icons[btype]} *{titles[btype]}:*")
        lines.append(f"   🏆 *{best['name']}*  ({best['bank']}){marker}")
        lines.append(f"   → {best['reward']['note']}")
        for r in group[1:]:
            lines.append(f"   • {r['name']}: {r['reward']['note']}")
        lines.append("")
        first_bucket = False

    top_card = next((buckets[b][0] for b in bucket_order if buckets[b]), None)
    if top_card:
        lines.append(f"💡 _{top_card['tip']}_")

    lines.append("\n⚠️ _Rates are approximate. Verify with your bank before deciding._")

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄  Try Another Category", callback_data="menu:recommend")],
        [InlineKeyboardButton("⬅️  Main Menu",            callback_data="back:main")],
    ])
    return "\n".join(lines), kb


# ── Central callback handler ──────────────────────────────────────────────────

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data  = query.data
    user_id = query.from_user.id

    # ── Navigation ──
    if data == "back:main":
        await query.answer()
        await query.edit_message_text(
            "Main menu — what would you like to do?",
            reply_markup=_main_menu_kb(),
        )
        return

    if data == "back:banks":
        await query.answer()
        await query.edit_message_text("🏦 Select your card's bank:", reply_markup=_bank_list_kb())
        return

    # ── Main menu items ──
    if data == "menu:addcard":
        await query.answer()
        await query.edit_message_text("🏦 Select your card's bank:", reply_markup=_bank_list_kb())
        return

    if data == "menu:mycards":
        await query.answer()
        card_ids = db.get_user_cards(user_id)
        text, kb = _my_cards_content(card_ids)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    if data == "menu:recommend":
        await query.answer()
        card_ids = db.get_user_cards(user_id)
        if not card_ids:
            await query.edit_message_text(
                "📭 You haven't added any cards yet. Add your cards first!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➕ Add a Card", callback_data="menu:addcard")],
                    [InlineKeyboardButton("⬅️ Back",       callback_data="back:main")],
                ]),
            )
            return
        await query.edit_message_text(
            "💡 *What are you spending on?*\n\nPick a category:",
            parse_mode="Markdown",
            reply_markup=_category_kb(),
        )
        return

    if data == "menu:pref":
        await query.answer()
        pref = db.get_reward_pref(user_id)
        labels = {"all": "Show all types", "cashback": "💰 Cashback", "miles": "✈️ Miles / Points"}
        current = labels.get(pref, "Show all types")
        text = (
            "*⚙️ Reward Preference*\n\n"
            "Choose which reward type to highlight in recommendations.\n\n"
            f"Current: *{current}*\n\n"
            "• *Show all* — display cashback, miles and points separately\n"
            "• *Prefer cashback* — highlight cashback cards first\n"
            "• *Prefer miles / points* — highlight miles & points cards first\n\n"
            "_Tip: miles are great if you fly Cathay/Asia Miles regularly and "
            "value 1 mile at ~HKD 0.15–0.25. Otherwise cashback is simpler._"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰  Prefer Cashback",      callback_data="pref:cashback")],
            [InlineKeyboardButton("✈️  Prefer Miles / Points", callback_data="pref:miles")],
            [InlineKeyboardButton("🔄  Show All Types",        callback_data="pref:all")],
            [InlineKeyboardButton("⬅️  Back",                  callback_data="back:main")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    if data.startswith("pref:"):
        pref = data[5:]
        if pref not in ("all", "cashback", "miles"):
            await query.answer()
            return
        db.set_reward_pref(user_id, pref)
        labels = {"all": "Show all types", "cashback": "💰 Prefer Cashback", "miles": "✈️ Prefer Miles / Points"}
        await query.answer(f"Saved: {labels[pref]}")
        await query.edit_message_text(
            f"✅ Preference saved: *{labels[pref]}*\n\nThis will highlight your preferred reward type at the top of every recommendation.",
            parse_mode="Markdown",
            reply_markup=_back_kb("main"),
        )
        return

    if data == "menu:help":
        await query.answer()
        text = (
            "*HK Credit Card Bot — Help* 🇭🇰\n\n"
            "*Commands:*\n"
            "/start — Open the main menu\n"
            "/addcard — Add a credit card\n"
            "/mycards — View & manage your cards\n"
            "/recommend — Get a spending recommendation\n\n"
            "*How it works:*\n"
            "1️⃣ Add your HK credit cards\n"
            "2️⃣ Pick a spending category\n"
            "3️⃣ See which card earns you the most!\n\n"
            "*Reward types:*\n"
            "💰 Cashback — % back on spending\n"
            "✈️ Miles — Air miles per HKD spent\n"
            "⭐ Points — Reward points per HKD\n\n"
            "Cards currently in the database:\n"
            f"  {len(CARDS)} cards across {len(BANKS)} banks\n\n"
            "⚠️ _Reward rates are approximate and change over time. "
            "Always verify with your bank before making financial decisions._"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=_back_kb("main"),
        )
        return

    # ── Bank selection ──
    if data.startswith("bank:"):
        await query.answer()
        bank_name = data[5:]
        if bank_name not in BANKS:
            await query.answer("Bank not found.", show_alert=True)
            return
        await query.edit_message_text(
            f"💳 Select a card from *{bank_name}*:",
            parse_mode="Markdown",
            reply_markup=_cards_for_bank_kb(bank_name),
        )
        return

    # ── Add card ──
    if data.startswith("addcard:"):
        card_id = data[8:]
        if card_id not in CARDS:
            await query.answer("Card not found.", show_alert=True)
            return
        card   = CARDS[card_id]
        added  = db.add_card(user_id, card_id)
        if added:
            await query.answer(f"✅ {card['name']} added!")
            msg = (
                f"✅ *{card['name']}* added to your wallet!\n\n"
                f"🏦 Bank: {card['bank']}\n"
                f"💎 Type: {card['reward_type'].title()}\n"
                f"📅 Annual Fee: {card['annual_fee']}\n\n"
                f"💡 {card['tip']}"
            )
        else:
            await query.answer("Already in your wallet.")
            msg = f"⚠️ *{card['name']}* is already in your wallet."

        await query.edit_message_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Another Card",   callback_data="back:banks")],
                [InlineKeyboardButton("💳 My Cards",           callback_data="menu:mycards")],
                [InlineKeyboardButton("⬅️ Main Menu",          callback_data="back:main")],
            ]),
        )
        return

    # ── Remove card ──
    if data.startswith("removecard:"):
        card_id   = data[11:]
        card_name = CARDS[card_id]["name"] if card_id in CARDS else card_id
        db.remove_card(user_id, card_id)
        await query.answer(f"Removed: {card_name}")
        card_ids  = db.get_user_cards(user_id)
        text, kb  = _my_cards_content(card_ids)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    # ── Category / recommendation ──
    if data.startswith("cat:"):
        await query.answer()
        category = data[4:]
        if category not in CATEGORIES:
            await query.answer("Unknown category.", show_alert=True)
            return
        card_ids = db.get_user_cards(user_id)
        if not card_ids:
            await query.answer("No cards added yet!", show_alert=True)
            return
        text, kb = _build_recommendation(user_id, category)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    # Fallback
    await query.answer()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    if not BOT_TOKEN:
        raise SystemExit("❌  BOT_TOKEN is not set. Copy .env.example to .env and add your token.")

    db.init_db()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("addcard",   cmd_addcard))
    app.add_handler(CommandHandler("mycards",   cmd_mycards))
    app.add_handler(CommandHandler("recommend", cmd_recommend))
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
