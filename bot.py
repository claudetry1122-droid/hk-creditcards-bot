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

def _equiv_str(sort_key: float, reward_type: str, card: dict, mile_value: float) -> str:
    """Return a short cashback-equivalent string for miles/points rates, or '' for cashback."""
    if reward_type == "miles":
        equiv = sort_key * mile_value * 100
        return f"≈ {equiv:.1f}% equiv"
    if reward_type == "points" and card.get("point_value_hkd"):
        equiv = sort_key * card["point_value_hkd"] * 100
        return f"≈ {equiv:.1f}% equiv"
    return ""


def _get_reward(card: dict, category: str) -> dict:
    """Return reward dict for category, falling back to parent then general."""
    if category in card["rewards"]:
        return card["rewards"][category]
    parent = CATEGORIES[category].get("parent")
    if parent and parent in card["rewards"]:
        return card["rewards"][parent]
    return card["rewards"]["general"]


# ── Keyboard builders ─────────────────────────────────────────────────────────

def _main_menu_kb(user_id: int | None = None):
    travel = db.get_travel_mode(user_id) if user_id else False
    travel_label = "✈️ Travel Mode: ON  ←" if travel else "🌏 Travel Mode: OFF"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕  Add a Card",          callback_data="menu:addcard")],
        [InlineKeyboardButton("💳  My Cards",            callback_data="menu:mycards")],
        [InlineKeyboardButton("💡  Get Recommendation",  callback_data="menu:recommend")],
        [InlineKeyboardButton(travel_label,              callback_data="menu:travel")],
        [InlineKeyboardButton("⚙️  Reward Preference",   callback_data="menu:pref")],
        [InlineKeyboardButton("🔍  Suggest New Cards",   callback_data="menu:suggest")],
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
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=_main_menu_kb(update.effective_user.id))


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


async def cmd_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.init_db()
    user_id = update.effective_user.id
    card_ids = db.get_user_cards(user_id)
    if not card_ids:
        await update.message.reply_text(
            "📭 You haven't added any cards yet.\n\nAdd your cards first so I can suggest what's missing!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add a Card", callback_data="menu:addcard")]
            ]),
        )
        return
    text, kb = _build_suggestions(user_id)
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
    travel = db.get_travel_mode(user_id)
    header = "✈️ *Travel mode active — overseas categories first!*\n\nWhat are you spending on?" if travel else "💡 *What are you spending on?*\n\nPick a category:"
    await update.message.reply_text(
        header,
        parse_mode="Markdown",
        reply_markup=_category_kb(travel),
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


def _category_kb(travel: bool = False) -> InlineKeyboardMarkup:
    # Ordered display: top-level first, then sub-categories grouped logically
    # In travel mode, overseas/japan/hotels/travel categories float to the top
    base_ordered = [
        "dining", "dining_fastfood", "dining_delivery",
        "online", "online_fashion", "supermarket_hktvmall",
        "supermarket", "supermarket_parknshop", "supermarket_health_beauty",
        "transport", "transport_mtr_bus",
        "travel", "travel_cathay", "travel_klook", "hotels",
        "entertainment", "entertainment_cinema", "entertainment_streaming",
        "utilities", "utilities_telecom",
        "overseas", "overseas_japan",
        "general",
    ]
    if travel:
        travel_first = ["overseas", "overseas_japan", "hotels", "travel", "travel_cathay", "travel_klook"]
        rest = [c for c in base_ordered if c not in travel_first]
        ordered = travel_first + rest
    else:
        ordered = base_ordered
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


# ── Recommendation & suggestion logic ────────────────────────────────────────

def _build_recommendation(user_id: int, category: str) -> tuple[str, InlineKeyboardMarkup]:
    card_ids = db.get_user_cards(user_id)
    cat_info = CATEGORIES[category]
    pref = db.get_reward_pref(user_id)
    travel = db.get_travel_mode(user_id)
    mile_value = db.get_mile_value(user_id)
    is_overseas_cat = category in ("overseas", "overseas_japan", "hotels", "travel", "travel_cathay", "travel_klook")

    buckets: dict[str, list[dict]] = {"cashback": [], "miles": [], "points": []}

    for card_id in card_ids:
        card = CARDS.get(card_id)
        if not card:
            continue
        reward = _get_reward(card, category)
        buckets[card["reward_type"]].append({
            "name":      card["name"],
            "bank":      card["bank"],
            "reward":    reward,
            "tip":       card["tip"],
            "card_id":   card_id,
            "cap_note":  card.get("cap_note"),
            "no_fx_fee": card.get("no_fx_fee", False),
            "card_obj":  card,
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
    if travel:
        lines.append("_✈️ Travel mode active_\n")
    elif pref_label:
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
        fx_badge = "  ✅ _No FX fee_" if (best["no_fx_fee"] and (travel or is_overseas_cat)) else ""
        lines.append(f"   🏆 *{best['name']}*  ({best['bank']}){marker}{fx_badge}")
        equiv = _equiv_str(best["reward"]["sort_key"], btype, best["card_obj"], mile_value)
        equiv_tag = f"  _({equiv})_" if equiv else ""
        lines.append(f"   → {best['reward']['note']}{equiv_tag}")
        if best["cap_note"]:
            lines.append(f"   ⚠️ _{best['cap_note']}_")
        for r in group[1:]:
            fx = "  ✅" if (r["no_fx_fee"] and (travel or is_overseas_cat)) else ""
            equiv = _equiv_str(r["reward"]["sort_key"], btype, r["card_obj"], mile_value)
            equiv_tag = f"  _({equiv})_" if equiv else ""
            lines.append(f"   • {r['name']}{fx}: {r['reward']['note']}{equiv_tag}")
            if r["cap_note"]:
                lines.append(f"     ⚠️ _{r['cap_note']}_")
        lines.append("")
        first_bucket = False

    top_card = next((buckets[b][0] for b in bucket_order if buckets[b]), None)
    if top_card:
        lines.append(f"💡 _{top_card['tip']}_")

    lines.append("\n⚠️ _Rates are approximate. Verify with your bank before deciding._")

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄  Try Another Category", callback_data="menu:recommend")],
        [InlineKeyboardButton("🔍  Suggest New Cards",    callback_data="menu:suggest")],
        [InlineKeyboardButton("⬅️  Main Menu",            callback_data="back:main")],
    ])
    return "\n".join(lines), kb


def _build_suggestions(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    user_card_ids = set(db.get_user_cards(user_id))
    pref = db.get_reward_pref(user_id)
    travel = db.get_travel_mode(user_id)

    missing = {cid: card for cid, card in CARDS.items() if cid not in user_card_ids}

    if not missing:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Main Menu", callback_data="back:main")]])
        return "✅ You already have all cards in our database — nothing left to suggest!", kb

    top_cats = [c for c, info in CATEGORIES.items() if info["parent"] is None and c != "general"]

    # Score each missing card by how much it improves the user's coverage per reward type
    type_groups: dict[str, list] = {"cashback": [], "miles": [], "points": []}

    for card_id, card in missing.items():
        rtype = card["reward_type"]

        # User's current best sort_key per top-level category for THIS reward type
        user_bests: dict[str, float] = {}
        for cat in top_cats:
            user_bests[cat] = max(
                (_get_reward(CARDS[uid], cat)["sort_key"]
                 for uid in user_card_ids if uid in CARDS and CARDS[uid]["reward_type"] == rtype),
                default=0.0,
            )

        # Find categories where this card beats the user's current best
        wins = []
        for cat in top_cats:
            card_rate = _get_reward(card, cat)["sort_key"]
            if card_rate > user_bests[cat]:
                improvement = card_rate - user_bests[cat]
                wins.append((improvement, cat, _get_reward(card, cat)["note"]))

        if wins:
            wins.sort(reverse=True)
            score = sum(w[0] for w in wins)
            if travel and card.get("no_fx_fee"):
                score *= 1.5  # boost travel-friendly cards in travel mode
            type_groups[rtype].append((score, card_id, card, wins[:3]))

    for g in type_groups.values():
        g.sort(reverse=True)

    # Display order based on preference
    if pref == "cashback":
        order = ["cashback", "miles", "points"]
    elif pref == "miles":
        order = ["miles", "points", "cashback"]
    else:
        order = ["cashback", "miles", "points"]

    lines = ["🔍 *Cards Worth Adding*\n"]
    if travel:
        lines.append("_✈️ Travel mode: overseas-friendly cards boosted_\n")

    icons = {"cashback": "💰", "miles": "✈️", "points": "⭐"}
    shown = 0

    for rtype in order:
        group = type_groups[rtype]
        if not group or shown >= 4:
            break
        _score, card_id, card, wins = group[0]
        lines.append(f"{icons[rtype]} *{card['name']}*  ({card['bank']})")
        lines.append(f"   Type: {card['reward_type'].title()} | Fee: {card['annual_fee']}")
        lines.append(f"   Best at:")
        for _, cat, note in wins[:2]:
            cat_info = CATEGORIES[cat]
            lines.append(f"   • {cat_info['emoji']} {cat_info['label']}: {note}")
        if card.get("cap_note"):
            lines.append(f"   ⚠️ _{card['cap_note']}_")
        if card.get("no_fx_fee"):
            lines.append(f"   ✅ _No FX fee_")
        lines.append("")
        shown += 1

    if shown == 0:
        lines = ["✅ Your current wallet already covers all categories well — no major gaps found!"]
    else:
        lines.append("_Tap ➕ Add a Card from the main menu to add any of the above._")

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕  Add a Card",  callback_data="menu:addcard")],
        [InlineKeyboardButton("⬅️  Main Menu",  callback_data="back:main")],
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
            reply_markup=_main_menu_kb(user_id),
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
        travel = db.get_travel_mode(user_id)
        header = "✈️ *Travel mode active — overseas categories first!*\n\nWhat are you spending on?" if travel else "💡 *What are you spending on?*\n\nPick a category:"
        await query.edit_message_text(
            header,
            parse_mode="Markdown",
            reply_markup=_category_kb(travel),
        )
        return

    if data == "menu:travel":
        await query.answer()
        travel = db.get_travel_mode(user_id)
        new_travel = not travel
        db.set_travel_mode(user_id, new_travel)
        if new_travel:
            msg = (
                "✈️ *Travel Mode ON*\n\n"
                "Overseas categories will appear first when you get a recommendation.\n"
                "Cards with *no FX fee* are highlighted.\n\n"
                "Safe travels! 🌏"
            )
        else:
            msg = "🏠 *Travel Mode OFF*\n\nBack to normal mode. Enjoy your local spending!"
        await query.edit_message_text(
            msg,
            parse_mode="Markdown",
            reply_markup=_main_menu_kb(user_id),
        )
        return

    if data == "menu:suggest":
        await query.answer()
        card_ids = db.get_user_cards(user_id)
        if not card_ids:
            await query.edit_message_text(
                "📭 You haven't added any cards yet.\n\nAdd your cards first so I can suggest what's missing!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➕ Add a Card", callback_data="menu:addcard")],
                    [InlineKeyboardButton("⬅️ Back",       callback_data="back:main")],
                ]),
            )
            return
        text, kb = _build_suggestions(user_id)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    if data == "menu:pref":
        await query.answer()
        pref = db.get_reward_pref(user_id)
        mile_value = db.get_mile_value(user_id)
        pref_labels = {"all": "Show all types", "cashback": "💰 Cashback", "miles": "✈️ Miles / Points"}
        current_pref = pref_labels.get(pref, "Show all types")
        text = (
            "*⚙️ Reward Preference*\n\n"
            f"Reward type shown first: *{current_pref}*\n"
            f"Mile value assumption: *HKD {mile_value:.2f} per mile*\n\n"
            "• *Show all* — display cashback, miles and points separately\n"
            "• *Prefer cashback* — highlight cashback cards first\n"
            "• *Prefer miles / points* — highlight miles & points cards first\n\n"
            "The *mile value* is used to show a cashback-equivalent % next to "
            "every miles/points rate in recommendations, so you can compare apples to apples.\n\n"
            "_HKD 0.15 = conservative (economy redemptions)\n"
            "HKD 0.20 = moderate (good economy / basic biz)\n"
            "HKD 0.25 = optimistic (business class redemptions)_"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰  Prefer Cashback",       callback_data="pref:cashback")],
            [InlineKeyboardButton("✈️  Prefer Miles / Points",  callback_data="pref:miles")],
            [InlineKeyboardButton("🔄  Show All Types",         callback_data="pref:all")],
            [InlineKeyboardButton("── Mile Value ──",           callback_data="noop")],
            [InlineKeyboardButton("HKD 0.10  (low)",           callback_data="mileval:0.10"),
             InlineKeyboardButton("HKD 0.15  (default)",       callback_data="mileval:0.15")],
            [InlineKeyboardButton("HKD 0.20  (good)",          callback_data="mileval:0.20"),
             InlineKeyboardButton("HKD 0.25  (premium)",       callback_data="mileval:0.25")],
            [InlineKeyboardButton("⬅️  Back",                   callback_data="back:main")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    if data == "noop":
        await query.answer()
        return

    if data.startswith("mileval:"):
        try:
            value = float(data[8:])
        except ValueError:
            await query.answer()
            return
        if value not in (0.10, 0.15, 0.20, 0.25):
            await query.answer()
            return
        db.set_mile_value(user_id, value)
        await query.answer(f"Mile value set to HKD {value:.2f}")
        # Re-open the pref screen with updated values shown
        pref = db.get_reward_pref(user_id)
        pref_labels = {"all": "Show all types", "cashback": "💰 Cashback", "miles": "✈️ Miles / Points"}
        current_pref = pref_labels.get(pref, "Show all types")
        text = (
            "*⚙️ Reward Preference*\n\n"
            f"Reward type shown first: *{current_pref}*\n"
            f"Mile value assumption: *HKD {value:.2f} per mile* ✅\n\n"
            "• *Show all* — display cashback, miles and points separately\n"
            "• *Prefer cashback* — highlight cashback cards first\n"
            "• *Prefer miles / points* — highlight miles & points cards first\n\n"
            "The *mile value* is used to show a cashback-equivalent % next to "
            "every miles/points rate in recommendations, so you can compare apples to apples.\n\n"
            "_HKD 0.15 = conservative (economy redemptions)\n"
            "HKD 0.20 = moderate (good economy / basic biz)\n"
            "HKD 0.25 = optimistic (business class redemptions)_"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰  Prefer Cashback",       callback_data="pref:cashback")],
            [InlineKeyboardButton("✈️  Prefer Miles / Points",  callback_data="pref:miles")],
            [InlineKeyboardButton("🔄  Show All Types",         callback_data="pref:all")],
            [InlineKeyboardButton("── Mile Value ──",           callback_data="noop")],
            [InlineKeyboardButton("HKD 0.10  (low)",           callback_data="mileval:0.10"),
             InlineKeyboardButton("HKD 0.15  (default)",       callback_data="mileval:0.15")],
            [InlineKeyboardButton("HKD 0.20  (good)",          callback_data="mileval:0.20"),
             InlineKeyboardButton("HKD 0.25  (premium)",       callback_data="mileval:0.25")],
            [InlineKeyboardButton("⬅️  Back",                   callback_data="back:main")],
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
            reply_markup=_main_menu_kb(user_id),
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
            "/recommend — Get a spending recommendation\n"
            "/suggest — Suggest cards to add\n\n"
            "*How it works:*\n"
            "1️⃣ Add your HK credit cards\n"
            "2️⃣ Pick a spending category\n"
            "3️⃣ See which card earns you the most!\n\n"
            "*Reward types:*\n"
            "💰 Cashback — % back on spending\n"
            "✈️ Miles — Air miles per HKD spent\n"
            "⭐ Points — Reward points per HKD\n\n"
            "*Features:*\n"
            "🌏 Travel Mode — Highlights overseas cards & no-FX-fee cards when abroad\n"
            "⚠️ Spending caps shown inline for capped cards\n"
            "🔍 Card suggestions based on your wallet gaps\n\n"
            f"Cards in database: {len(CARDS)} across {len(BANKS)} banks\n\n"
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
    app.add_handler(CommandHandler("suggest",   cmd_suggest))
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
