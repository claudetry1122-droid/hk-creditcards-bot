"""
HK Credit Card reward data.

reward_type:
  "cashback" → rate is cashback %
  "miles"    → rate is miles earned per HKD 1 spent
  "points"   → rate is reward points per HKD 1 spent

sort_key: used to rank cards within the same reward_type group.

parent: for sub-categories, the key of the parent category to fall back to
        when a card has no explicit entry for this sub-category.
        None for top-level categories.

⚠️  Rates are approximate and change frequently.
    Always verify current terms with the issuing bank.
"""

CATEGORIES = {
    # ── Top-level categories ───────────────────────────────────────────────
    "dining":        {"emoji": "🍽️",  "label": "Dining",           "parent": None},
    "online":        {"emoji": "🛒",   "label": "Online Shopping",  "parent": None},
    "travel":        {"emoji": "✈️",   "label": "Travel",           "parent": None},
    "hotels":        {"emoji": "🏨",   "label": "Hotels",           "parent": None},
    "supermarket":   {"emoji": "🛍️",  "label": "Supermarkets",     "parent": None},
    "transport":     {"emoji": "🚕",   "label": "Transport",        "parent": None},
    "utilities":     {"emoji": "💡",   "label": "Utilities & Bills","parent": None},
    "entertainment": {"emoji": "🎬",   "label": "Entertainment",    "parent": None},
    "overseas":      {"emoji": "🌏",   "label": "Overseas / FX",    "parent": None},
    "general":       {"emoji": "💳",   "label": "General",          "parent": None},

    # ── Dining sub-categories ──────────────────────────────────────────────
    "dining_fastfood":  {"emoji": "🍔", "label": "Fast Food",        "parent": "dining"},
    "dining_delivery":  {"emoji": "🛵", "label": "Food Delivery",    "parent": "dining"},

    # ── Online / shopping sub-categories ──────────────────────────────────
    "online_fashion":   {"emoji": "👗", "label": "Fashion Online",   "parent": "online"},

    # ── Supermarket sub-categories ─────────────────────────────────────────
    "supermarket_parknshop":     {"emoji": "🏪", "label": "PARKnSHOP/Circle K",   "parent": "supermarket"},
    "supermarket_health_beauty": {"emoji": "💊", "label": "Mannings/Watsons/Sasa","parent": "supermarket"},
    "supermarket_hktvmall":      {"emoji": "📦", "label": "HKTVmall",             "parent": "online"},

    # ── Transport sub-categories ───────────────────────────────────────────
    "transport_mtr_bus": {"emoji": "🚇", "label": "MTR/Bus/Tram",    "parent": "transport"},

    # ── Travel sub-categories ──────────────────────────────────────────────
    "travel_cathay": {"emoji": "🐉", "label": "Cathay/HK Express",   "parent": "travel"},
    "travel_klook":  {"emoji": "🎫", "label": "Klook/Travel Booking","parent": "online"},

    # ── Entertainment sub-categories ──────────────────────────────────────
    "entertainment_cinema":    {"emoji": "🎭", "label": "Cinema",      "parent": "entertainment"},
    "entertainment_streaming": {"emoji": "📺", "label": "Streaming",   "parent": "online"},

    # ── Utilities sub-categories ───────────────────────────────────────────
    "utilities_telecom": {"emoji": "📱", "label": "Telecom",           "parent": "utilities"},

    # ── Overseas sub-categories ────────────────────────────────────────────
    "overseas_japan": {"emoji": "🗾", "label": "Japan",                "parent": "overseas"},
}

CARDS = {
    # ── HSBC ──────────────────────────────────────────────────────────────────
    "hsbc_red": {
        "name": "HSBC Red Credit Card",
        "bank": "HSBC",
        "reward_type": "cashback",
        "annual_fee": "Perpetual waiver (no spend requirement)",
        "rewards": {
            "dining":        {"rate": 8.0,  "note": "Up to 8% at designated dining merchants (HKD 1,250/month cap)",  "sort_key": 8.0},
            "online":        {"rate": 4.0,  "note": "4% cashback on online spending (HKD 10,000/month cap)",          "sort_key": 4.0},
            "travel":        {"rate": 8.0,  "note": "Up to 8% at designated travel merchants (cap applies)",          "sort_key": 8.0},
            "hotels":        {"rate": 8.0,  "note": "Up to 8% at designated hotel merchants (cap applies)",           "sort_key": 8.0},
            "supermarket":   {"rate": 8.0,  "note": "Up to 8% at designated supermarket merchants (cap applies)",     "sort_key": 8.0},
            "transport":     {"rate": 0.4,  "note": "0.4% cashback (base rate)",                                      "sort_key": 0.4},
            "utilities":     {"rate": 0.4,  "note": "0.4% cashback (base rate)",                                      "sort_key": 0.4},
            "entertainment": {"rate": 8.0,  "note": "Up to 8% at designated entertainment merchants (cap applies)",   "sort_key": 8.0},
            "overseas":      {"rate": 0.4,  "note": "0.4% cashback (base rate)",                                      "sort_key": 0.4},
            "general":       {"rate": 0.4,  "note": "0.4% cashback (base rate)",                                      "sort_key": 0.4},
        },
        "tip": "8% at designated merchants (dining/shopping/entertainment); 4% all online; 0.4% elsewhere. Perpetual fee waiver. Min income HKD 120k.",
        "cap_note": "8% cashback capped at HKD 1,250/month; 4% online capped at HKD 10,000/month",
        "no_fx_fee": True,
    },
    "hsbc_visa_sig": {
        "name": "HSBC Visa Signature Credit Card",
        "bank": "HSBC",
        "reward_type": "cashback",
        "annual_fee": "HKD 2,000 (first 2-year waiver for new cardholders)",
        "rewards": {
            "dining":        {"rate": 3.6,  "note": "Up to 3.6% RewardCash if chosen as bonus category",  "sort_key": 3.6},
            "online":        {"rate": 3.6,  "note": "Up to 3.6% RewardCash if chosen as bonus category",  "sort_key": 3.6},
            "travel":        {"rate": 3.6,  "note": "Up to 3.6% RewardCash if chosen as bonus category",  "sort_key": 3.6},
            "hotels":        {"rate": 3.6,  "note": "Up to 3.6% RewardCash if chosen as bonus category",  "sort_key": 3.6},
            "supermarket":   {"rate": 3.6,  "note": "Up to 3.6% RewardCash if chosen as bonus category",  "sort_key": 3.6},
            "transport":     {"rate": 0.4,  "note": "0.4% RewardCash (base rate)",                        "sort_key": 0.4},
            "utilities":     {"rate": 0.4,  "note": "0.4% RewardCash (base rate)",                        "sort_key": 0.4},
            "entertainment": {"rate": 3.6,  "note": "Up to 3.6% RewardCash if chosen as bonus category",  "sort_key": 3.6},
            "overseas":      {"rate": 0.4,  "note": "0.4% RewardCash (base rate)",                        "sort_key": 0.4},
            "general":       {"rate": 0.4,  "note": "0.4% RewardCash (base rate)",                        "sort_key": 0.4},
        },
        "tip": "Pick one bonus category for up to 3.6% RewardCash; 0.4% on everything else. Redeemable as statement credit. Min income HKD 240k.",
    },
    "hsbc_everymile": {
        "name": "HSBC EveryMile Credit Card",
        "bank": "HSBC",
        "reward_type": "miles",
        "annual_fee": "HKD 2,000 (first-year waiver for new cardholders)",
        "rewards": {
            "dining":        {"rate": 0.5,  "note": "HKD 2 = 1 EveryMile at café & light meal merchants",      "sort_key": 0.5},
            "online":        {"rate": 0.2,  "note": "HKD 5 = 1 EveryMile (general rate)",                      "sort_key": 0.2},
            "travel":        {"rate": 0.5,  "note": "HKD 2 = 1 EveryMile on travel & cross-border merchants",  "sort_key": 0.5},
            "hotels":        {"rate": 0.5,  "note": "HKD 2 = 1 EveryMile on hotel merchants",                  "sort_key": 0.5},
            "supermarket":   {"rate": 0.2,  "note": "HKD 5 = 1 EveryMile (general rate)",                      "sort_key": 0.2},
            "transport":     {"rate": 0.5,  "note": "HKD 2 = 1 EveryMile on local transport",                  "sort_key": 0.5},
            "utilities":     {"rate": 0.2,  "note": "HKD 5 = 1 EveryMile (general rate)",                      "sort_key": 0.2},
            "entertainment": {"rate": 0.2,  "note": "HKD 5 = 1 EveryMile (general rate)",                      "sort_key": 0.2},
            "overseas":      {"rate": 0.5,  "note": "HKD 2 = 1 EveryMile on cross-border & overseas",          "sort_key": 0.5},
            "general":       {"rate": 0.2,  "note": "HKD 5 = 1 EveryMile (general rate)",                      "sort_key": 0.2},
            # Sub-categories
            "transport_mtr_bus": {"rate": 0.5,  "note": "HKD 2 = 1 EveryMile on local transit",               "sort_key": 0.5},
            "travel_cathay":     {"rate": 0.5,  "note": "HKD 2 = 1 EveryMile on Cathay/HK Express",           "sort_key": 0.5},
        },
        "tip": "HKD 2 = 1 mile on café, local transport, cross-border & travel; HKD 5 = 1 mile on everything else. Includes lounge access. Min income HKD 240k.",
        "no_fx_fee": True,
    },

    # ── HANG SENG ─────────────────────────────────────────────────────────────
    "hangseng_enjoy": {
        "name": "Hang Seng yuu Mastercard",
        "bank": "Hang Seng",
        "reward_type": "points",
        "annual_fee": "Free",
        "rewards": {
            # Base rates — bonus applies only at specific yuu partner chains
            "dining":        {"rate": 1.0,  "note": "1 yuu Point/HKD (base; 4 pts at KFC/Pizza Hut/Maxim's)",     "sort_key": 1.0},
            "online":        {"rate": 2.0,  "note": "2 yuu Points/HKD on online spending",                         "sort_key": 2.0},
            "travel":        {"rate": 1.0,  "note": "1 yuu Point/HKD (base rate)",                                 "sort_key": 1.0},
            "hotels":        {"rate": 1.0,  "note": "1 yuu Point/HKD (base rate)",                                 "sort_key": 1.0},
            "supermarket":   {"rate": 1.0,  "note": "1 yuu Point/HKD (base; 3 pts at Mannings)",                   "sort_key": 1.0},
            "transport":     {"rate": 1.0,  "note": "1 yuu Point/HKD (base rate)",                                 "sort_key": 1.0},
            "utilities":     {"rate": 1.0,  "note": "1 yuu Point/HKD (base rate)",                                 "sort_key": 1.0},
            "entertainment": {"rate": 1.0,  "note": "1 yuu Point/HKD (base rate)",                                 "sort_key": 1.0},
            "overseas":      {"rate": 1.0,  "note": "1 yuu Point/HKD (base rate)",                                 "sort_key": 1.0},
            "general":       {"rate": 1.0,  "note": "1 yuu Point/HKD (base rate)",                                 "sort_key": 1.0},
            # Sub-categories with specific yuu partner rates
            "dining_fastfood":          {"rate": 4.0, "note": "4 yuu Points/HKD at KFC, Pizza Hut & Maxim's",   "sort_key": 4.0},
            "supermarket_health_beauty":{"rate": 3.0, "note": "3 yuu Points/HKD at Mannings (200 pts = HKD 1)", "sort_key": 3.0},
            "supermarket_parknshop":    {"rate": 1.0, "note": "1 yuu Point/HKD at PARKnSHOP (base rate)",       "sort_key": 1.0},
        },
        "tip": "4 pts/HKD at KFC/Pizza Hut/Maxim's; 3 pts/HKD at Mannings; 2 pts/HKD online; 1 pt/HKD base. 200 yuu Points = HKD 1. Free annual fee.",
    },
    "hangseng_mpower": {
        "name": "Hang Seng MMPOWER World Mastercard",
        "bank": "Hang Seng",
        "reward_type": "cashback",
        "annual_fee": "Free (for eligible customers)",
        "rewards": {
            "dining":        {"rate": 2.0,  "note": "Up to 2% +FUN Dollars on dining",                  "sort_key": 2.0},
            "online":        {"rate": 8.0,  "note": "Up to 8% +FUN Dollars on online shopping",         "sort_key": 8.0},
            "travel":        {"rate": 1.0,  "note": "1% +FUN Dollars on travel",                        "sort_key": 1.0},
            "hotels":        {"rate": 1.0,  "note": "1% +FUN Dollars on hotels",                        "sort_key": 1.0},
            "supermarket":   {"rate": 1.0,  "note": "1% +FUN Dollars on supermarkets",                  "sort_key": 1.0},
            "transport":     {"rate": 0.4,  "note": "0.4% +FUN Dollars (base rate)",                    "sort_key": 0.4},
            "utilities":     {"rate": 0.4,  "note": "0.4% +FUN Dollars (base rate)",                    "sort_key": 0.4},
            "entertainment": {"rate": 8.0,  "note": "Up to 8% +FUN Dollars on entertainment",           "sort_key": 8.0},
            "overseas":      {"rate": 1.0,  "note": "1% +FUN Dollars overseas",                         "sort_key": 1.0},
            "general":       {"rate": 0.4,  "note": "0.4% +FUN Dollars (base rate)",                    "sort_key": 0.4},
            # Sub-categories
            "online_fashion":          {"rate": 8.0, "note": "Up to 8% +FUN Dollars on fashion & clothing online", "sort_key": 8.0},
            "entertainment_cinema":    {"rate": 8.0, "note": "Up to 8% +FUN Dollars on cinema",                    "sort_key": 8.0},
            "entertainment_streaming": {"rate": 8.0, "note": "Up to 8% +FUN Dollars on streaming (online)",        "sort_key": 8.0},
        },
        "tip": "Up to 8% +FUN Dollars on online shopping, fashion & entertainment. Redeemable at Hang Seng partners. No annual fee for eligible customers.",
    },

    # ── CITI ──────────────────────────────────────────────────────────────────
    "citi_cashback": {
        "name": "Citi Cash Back Credit Card",
        "bank": "Citi",
        "reward_type": "cashback",
        "annual_fee": "HKD 1,800 (waivable with qualifying spend)",
        "rewards": {
            "dining":        {"rate": 2.0,  "note": "2% cashback on local dining",                 "sort_key": 2.0},
            "online":        {"rate": 1.0,  "note": "1% cashback",                                 "sort_key": 1.0},
            "travel":        {"rate": 2.0,  "note": "2% cashback on foreign currency travel",      "sort_key": 2.0},
            "hotels":        {"rate": 2.0,  "note": "2% cashback on local & overseas hotels",      "sort_key": 2.0},
            "supermarket":   {"rate": 1.0,  "note": "1% cashback",                                 "sort_key": 1.0},
            "transport":     {"rate": 1.0,  "note": "1% cashback",                                 "sort_key": 1.0},
            "utilities":     {"rate": 1.0,  "note": "1% cashback",                                 "sort_key": 1.0},
            "entertainment": {"rate": 1.0,  "note": "1% cashback",                                 "sort_key": 1.0},
            "overseas":      {"rate": 2.0,  "note": "2% cashback on all foreign currency spend",   "sort_key": 2.0},
            "general":       {"rate": 1.0,  "note": "1% cashback (base rate)",                     "sort_key": 1.0},
        },
        "tip": "2% on local dining, hotels and all foreign currency transactions. Simple cashback with no tricky tiers.",
    },
    "citi_rewards": {
        "name": "Citi Rewards Credit Card",
        "bank": "Citi",
        "reward_type": "points",
        "annual_fee": "HKD 1,800 (waivable)",
        "rewards": {
            "dining":        {"rate": 1.0,  "note": "1 Citi Point/HKD",                                               "sort_key": 1.0},
            "online":        {"rate": 1.0,  "note": "1 Citi Point/HKD (general online)",                              "sort_key": 1.0},
            "travel":        {"rate": 1.0,  "note": "1 Citi Point/HKD",                                               "sort_key": 1.0},
            "hotels":        {"rate": 1.0,  "note": "1 Citi Point/HKD",                                               "sort_key": 1.0},
            "supermarket":   {"rate": 3.0,  "note": "3 Citi Points/HKD at department stores & selected retail",       "sort_key": 3.0},
            "transport":     {"rate": 1.0,  "note": "1 Citi Point/HKD",                                               "sort_key": 1.0},
            "utilities":     {"rate": 1.0,  "note": "1 Citi Point/HKD",                                               "sort_key": 1.0},
            "entertainment": {"rate": 3.0,  "note": "3 Citi Points/HKD on movies & entertainment",                    "sort_key": 3.0},
            "overseas":      {"rate": 1.0,  "note": "1 Citi Point/HKD",                                               "sort_key": 1.0},
            "general":       {"rate": 1.0,  "note": "1 Citi Point/HKD (base rate)",                                   "sort_key": 1.0},
            # Sub-categories
            "online_fashion":          {"rate": 3.0, "note": "3 Citi Points/HKD on fashion & clothing (dept store)", "sort_key": 3.0},
            "entertainment_cinema":    {"rate": 3.0, "note": "3 Citi Points/HKD on cinema tickets",                  "sort_key": 3.0},
            "entertainment_streaming": {"rate": 3.0, "note": "3 Citi Points/HKD on streaming subscriptions",         "sort_key": 3.0},
        },
        "tip": "3x Citi Points on entertainment (movies/streaming), shopping (dept stores, fashion). Points convertible to Asia Miles.",
    },
    "citi_premiermiles": {
        "name": "Citi PremierMiles Card",
        "bank": "Citi",
        "reward_type": "miles",
        "annual_fee": "HKD 1,800 (waivable)",
        "rewards": {
            "dining":        {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (local spend)",                              "sort_key": 0.125},
            "online":        {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (local spend)",                              "sort_key": 0.125},
            "travel":        {"rate": 0.333, "note": "HKD 3 = 1 Citi Mile overseas (HKD 20k+/month); HKD 4 below",    "sort_key": 0.333},
            "hotels":        {"rate": 0.333, "note": "HKD 3 = 1 Citi Mile overseas (HKD 20k+/month); HKD 4 below",    "sort_key": 0.333},
            "supermarket":   {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (local spend)",                              "sort_key": 0.125},
            "transport":     {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (local spend)",                              "sort_key": 0.125},
            "utilities":     {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (local spend)",                              "sort_key": 0.125},
            "entertainment": {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (local spend)",                              "sort_key": 0.125},
            "overseas":      {"rate": 0.333, "note": "HKD 3 = 1 Citi Mile overseas with HKD 20k+/month total spend",  "sort_key": 0.333},
            "general":       {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (local spend)",                              "sort_key": 0.125},
            # Sub-categories
            "travel_cathay": {"rate": 0.125, "note": "HKD 8 = 1 Citi Mile (Cathay booked locally in HKD)",            "sort_key": 0.125},
        },
        "tip": "Citi Miles transferable to Asia Miles and 10+ partners. Best overseas rate (HKD 3 = 1 mile) with HKD 20k+/month spend. Cathay booked locally earns the HKD 8 rate.",
    },

    # ── STANDARD CHARTERED ────────────────────────────────────────────────────
    "sc_smart": {
        "name": "Standard Chartered Smart Credit Card",
        "bank": "Standard Chartered",
        "reward_type": "cashback",
        "annual_fee": "Free",
        "rewards": {
            # General rates (non-designated merchants): 1.2%
            # Designated merchants earn 5%: HKTVmall, Circle K, PARKnSHOP, Watsons, Sasa,
            # McDonald's HK, Foodpanda, Klook, China Mobile HK, s/ash
            "dining":        {"rate": 1.2,  "note": "1.2% cashback (general restaurants; 5% at McDonald's HK)",    "sort_key": 1.2},
            "online":        {"rate": 1.2,  "note": "1.2% cashback (general online; 5% at HKTVmall/Klook)",        "sort_key": 1.2},
            "travel":        {"rate": 1.2,  "note": "1.2% cashback (general; 5% at Klook)",                        "sort_key": 1.2},
            "hotels":        {"rate": 1.2,  "note": "1.2% cashback (general rate)",                                "sort_key": 1.2},
            "supermarket":   {"rate": 1.2,  "note": "1.2% cashback (general; 5% at PARKnSHOP/Circle K/Watsons/Sasa)", "sort_key": 1.2},
            "transport":     {"rate": 1.2,  "note": "1.2% cashback (general rate); zero FX fee",                  "sort_key": 1.2},
            "utilities":     {"rate": 1.2,  "note": "1.2% cashback (general; 5% at China Mobile HK)",             "sort_key": 1.2},
            "entertainment": {"rate": 1.2,  "note": "1.2% cashback (general; 5% at s/ash)",                       "sort_key": 1.2},
            "overseas":      {"rate": 1.2,  "note": "1.2% cashback on FX transactions; zero FX fee",              "sort_key": 1.2},
            "general":       {"rate": 1.2,  "note": "1.2% cashback (base rate)",                                   "sort_key": 1.2},
            # Sub-categories at designated merchant 5% rate
            "dining_fastfood":          {"rate": 5.0, "note": "5% cashback at McDonald's HK (designated merchant)",               "sort_key": 5.0},
            "dining_delivery":          {"rate": 5.0, "note": "5% cashback via Foodpanda (designated); Deliveroo = 1.2%",         "sort_key": 5.0},
            "supermarket_parknshop":    {"rate": 5.0, "note": "5% cashback at PARKnSHOP & Circle K (designated merchants)",       "sort_key": 5.0},
            "supermarket_health_beauty":{"rate": 5.0, "note": "5% at Watsons & Sasa (designated); Mannings is NOT designated",    "sort_key": 5.0},
            "supermarket_hktvmall":     {"rate": 5.0, "note": "5% cashback at HKTVmall (designated online merchant)",             "sort_key": 5.0},
            "travel_klook":             {"rate": 5.0, "note": "5% cashback at Klook (designated merchant)",                       "sort_key": 5.0},
            "utilities_telecom":        {"rate": 5.0, "note": "5% cashback at China Mobile HK (designated merchant)",             "sort_key": 5.0},
            "entertainment_streaming":  {"rate": 1.2, "note": "1.2% cashback (streaming platforms not in designated list)",       "sort_key": 1.2},
        },
        "tip": "Free annual fee. Zero FX fee. 5% at 10 designated merchants: McDonald's, Foodpanda, HKTVmall, PARKnSHOP, Circle K, Watsons, Sasa, Klook, China Mobile HK, s/ash. 1.2% everywhere else.",
        "no_fx_fee": True,
    },
    "sc_cathay": {
        "name": "Standard Chartered Cathay Mastercard",
        "bank": "Standard Chartered",
        "reward_type": "miles",
        "annual_fee": "HKD 2,000 (waivable)",
        "rewards": {
            "dining":        {"rate": 0.25,  "note": "HKD 4 = 1 Asia Mile on dining",                         "sort_key": 0.25},
            "online":        {"rate": 0.167, "note": "HKD 6 = 1 Asia Mile (general rate)",                    "sort_key": 0.167},
            "travel":        {"rate": 0.5,   "note": "HKD 2 = 1 Asia Mile on Cathay Pacific & HK Express",    "sort_key": 0.5},
            "hotels":        {"rate": 0.25,  "note": "HKD 4 = 1 Asia Mile on hotels",                         "sort_key": 0.25},
            "supermarket":   {"rate": 0.167, "note": "HKD 6 = 1 Asia Mile (general rate)",                    "sort_key": 0.167},
            "transport":     {"rate": 0.167, "note": "HKD 6 = 1 Asia Mile (general rate)",                    "sort_key": 0.167},
            "utilities":     {"rate": 0.167, "note": "HKD 6 = 1 Asia Mile (general rate)",                    "sort_key": 0.167},
            "entertainment": {"rate": 0.167, "note": "HKD 6 = 1 Asia Mile (general rate)",                    "sort_key": 0.167},
            "overseas":      {"rate": 0.25,  "note": "HKD 4 = 1 Asia Mile on overseas spend",                 "sort_key": 0.25},
            "general":       {"rate": 0.167, "note": "HKD 6 = 1 Asia Mile (general rate)",                    "sort_key": 0.167},
            # Sub-category
            "travel_cathay": {"rate": 0.5,   "note": "HKD 2 = 1 Asia Mile on Cathay Pacific & HK Express",   "sort_key": 0.5},
        },
        "tip": "Best rate on Cathay/HK Express (HKD 2 = 1 Asia Mile). HKD 4 = 1 mile on dining, hotels & overseas. Earns Asia Miles directly.",
    },
    "sc_simply_cash": {
        "name": "Standard Chartered Simply Cash Credit Card",
        "bank": "Standard Chartered",
        "reward_type": "cashback",
        "annual_fee": "Free",
        "rewards": {
            "dining":        {"rate": 1.5,  "note": "1.5% cashback on local HKD spend",            "sort_key": 1.5},
            "online":        {"rate": 1.5,  "note": "1.5% cashback on local HKD spend",            "sort_key": 1.5},
            "travel":        {"rate": 2.0,  "note": "2.0% cashback on foreign currency bookings",  "sort_key": 2.0},
            "hotels":        {"rate": 2.0,  "note": "2.0% cashback on foreign currency payments",  "sort_key": 2.0},
            "supermarket":   {"rate": 1.5,  "note": "1.5% cashback on local HKD spend",            "sort_key": 1.5},
            "transport":     {"rate": 1.5,  "note": "1.5% cashback on local HKD spend",            "sort_key": 1.5},
            "utilities":     {"rate": 1.5,  "note": "1.5% cashback on local HKD spend",            "sort_key": 1.5},
            "entertainment": {"rate": 1.5,  "note": "1.5% cashback on local HKD spend",            "sort_key": 1.5},
            "overseas":      {"rate": 2.0,  "note": "2.0% cashback on all foreign currency spend", "sort_key": 2.0},
            "general":       {"rate": 1.5,  "note": "1.5% cashback on local HKD spend",            "sort_key": 1.5},
            # Sub-category
            "overseas_japan":{"rate": 2.0,  "note": "2.0% cashback (FX transaction)",              "sort_key": 2.0},
        },
        "tip": "Flat 1.5% local HKD; 2.0% on foreign currencies. No annual fee. Great no-fuss everyday card.",
    },

    # ── SIM ───────────────────────────────────────────────────────────────────
    "sim_credit": {
        "name": "sim Credit Card",
        "bank": "sim",
        "reward_type": "cashback",
        "annual_fee": "Free (perpetual waiver for full-time university/tertiary students)",
        "rewards": {
            "dining":        {"rate": 0.4,  "note": "0.4% cashback (base rate)",                        "sort_key": 0.4},
            "online":        {"rate": 8.0,  "note": "Up to 8% cashback on online spending",             "sort_key": 8.0},
            "travel":        {"rate": 8.0,  "note": "Up to 8% if booked online; 0.4% otherwise",        "sort_key": 8.0},
            "hotels":        {"rate": 8.0,  "note": "Up to 8% if booked online; 0.4% otherwise",        "sort_key": 8.0},
            "overseas":      {"rate": 0.4,  "note": "0.4% base (use sim World MC for overseas)",        "sort_key": 0.4},
            "supermarket":   {"rate": 0.4,  "note": "0.4% cashback (base rate)",                        "sort_key": 0.4},
            "transport":     {"rate": 8.0,  "note": "Up to 8% on CityBus/KMB/MTR/Tram/Star Ferry",     "sort_key": 8.0},
            "utilities":     {"rate": 2.0,  "note": "Up to 2% cashback on bill payments via app",       "sort_key": 2.0},
            "entertainment": {"rate": 8.0,  "note": "Up to 8% if purchased online",                     "sort_key": 8.0},
            "general":       {"rate": 0.4,  "note": "0.4% cashback (base rate)",                        "sort_key": 0.4},
            # Sub-categories
            "transport_mtr_bus":        {"rate": 8.0, "note": "Up to 8% on CityBus/KMB/MTR/Tram/Star Ferry", "sort_key": 8.0},
            "supermarket_hktvmall":     {"rate": 8.0, "note": "Up to 8% at HKTVmall (online transaction)",   "sort_key": 8.0},
            "entertainment_streaming":  {"rate": 8.0, "note": "Up to 8% on streaming (online transaction)",  "sort_key": 8.0},
            "travel_klook":             {"rate": 8.0, "note": "Up to 8% at Klook (online transaction)",      "sort_key": 8.0},
            "online_fashion":           {"rate": 8.0, "note": "Up to 8% on fashion online",                  "sort_key": 8.0},
        },
        "tip": "Best for online shopping & local transit (MTR/bus/tram). Requires HKD 1,000 non-online spend/month to unlock bonus; HKD 200/month cashback cap.",
        "cap_note": "Bonus cashback (above 0.4% base) capped at HKD 200/month combined",
    },
    "sim_world_mc": {
        "name": "sim World Mastercard®",
        "bank": "sim",
        "reward_type": "cashback",
        "annual_fee": "Free",
        "rewards": {
            "dining":        {"rate": 0.4,  "note": "0.4% cashback (base rate)",                          "sort_key": 0.4},
            "online":        {"rate": 8.0,  "note": "Up to 8% cashback on online spending",               "sort_key": 8.0},
            "travel":        {"rate": 8.0,  "note": "Up to 8% online or overseas bookings",               "sort_key": 8.0},
            "hotels":        {"rate": 8.0,  "note": "Up to 8% online or overseas hotels",                 "sort_key": 8.0},
            "overseas":      {"rate": 8.0,  "note": "Up to 8% on all overseas transactions",              "sort_key": 8.0},
            "supermarket":   {"rate": 0.4,  "note": "0.4% cashback (base rate)",                          "sort_key": 0.4},
            "transport":     {"rate": 0.4,  "note": "0.4% base (use sim Credit Card for local transit)",  "sort_key": 0.4},
            "utilities":     {"rate": 2.0,  "note": "Up to 2% cashback on bill payments via app",         "sort_key": 2.0},
            "entertainment": {"rate": 8.0,  "note": "Up to 8% if purchased online",                       "sort_key": 8.0},
            "general":       {"rate": 0.4,  "note": "0.4% cashback (base rate)",                          "sort_key": 0.4},
            # Sub-categories
            "overseas_japan":           {"rate": 8.0, "note": "Up to 8% on all overseas/Japan transactions",       "sort_key": 8.0},
            "supermarket_hktvmall":     {"rate": 8.0, "note": "Up to 8% at HKTVmall (online transaction)",         "sort_key": 8.0},
            "entertainment_streaming":  {"rate": 8.0, "note": "Up to 8% on streaming (online transaction)",        "sort_key": 8.0},
            "travel_klook":             {"rate": 8.0, "note": "Up to 8% at Klook (online transaction)",            "sort_key": 8.0},
            "online_fashion":           {"rate": 8.0, "note": "Up to 8% on fashion online",                        "sort_key": 8.0},
        },
        "tip": "Best for overseas spending & online shopping. Requires HKD 1,000 non-online spend/month to unlock bonus; HKD 200/month cashback cap.",
        "cap_note": "Bonus cashback (above 0.4% base) capped at HKD 200/month combined",
        "no_fx_fee": True,
    },

    # ── DBS ───────────────────────────────────────────────────────────────────
    "dbs_black": {
        "name": "DBS Black World Mastercard",
        "bank": "DBS",
        "reward_type": "miles",
        "annual_fee": "HKD 2,000 (waivable)",
        "rewards": {
            "dining":        {"rate": 0.167, "note": "HKD 6 = 1 DBS Dollar locally",                   "sort_key": 0.167},
            "online":        {"rate": 0.167, "note": "HKD 6 = 1 DBS Dollar locally",                   "sort_key": 0.167},
            "travel":        {"rate": 0.25,  "note": "HKD 4 = 1 DBS Dollar on overseas transactions",  "sort_key": 0.25},
            "hotels":        {"rate": 0.25,  "note": "HKD 4 = 1 DBS Dollar on overseas transactions",  "sort_key": 0.25},
            "supermarket":   {"rate": 0.167, "note": "HKD 6 = 1 DBS Dollar locally",                   "sort_key": 0.167},
            "transport":     {"rate": 0.167, "note": "HKD 6 = 1 DBS Dollar locally",                   "sort_key": 0.167},
            "utilities":     {"rate": 0.167, "note": "HKD 6 = 1 DBS Dollar locally",                   "sort_key": 0.167},
            "entertainment": {"rate": 0.167, "note": "HKD 6 = 1 DBS Dollar locally",                   "sort_key": 0.167},
            "overseas":      {"rate": 0.25,  "note": "HKD 4 = 1 DBS Dollar on all overseas spend",     "sort_key": 0.25},
            "general":       {"rate": 0.167, "note": "HKD 6 = 1 DBS Dollar (local general rate)",      "sort_key": 0.167},
            # Sub-category
            "overseas_japan":{"rate": 0.25,  "note": "HKD 4 = 1 DBS Dollar (overseas transaction)",    "sort_key": 0.25},
        },
        "tip": "HKD 4 = 1 mile on all overseas spending; HKD 6 = 1 mile locally. DBS Dollars convertible to Asia Miles and other rewards partners.",
    },

    # ── BOC (BANK OF CHINA) ───────────────────────────────────────────────────
    "boc_chill": {
        "name": "BOC Chill Credit Card",
        "bank": "BOC (Bank of China)",
        "reward_type": "cashback",
        "annual_fee": "Free",
        "rewards": {
            "dining":        {"rate": 10.0, "note": "Up to 10% at Chill Merchants — dining (World MC; HKD 1,500/month min)",  "sort_key": 10.0},
            "online":        {"rate": 5.0,  "note": "5% cashback on online spending (World MC); 4% Platinum MC",              "sort_key": 5.0},
            "travel":        {"rate": 0.5,  "note": "0.5% cashback (base rate)",                                              "sort_key": 0.5},
            "hotels":        {"rate": 0.5,  "note": "0.5% cashback (base rate)",                                              "sort_key": 0.5},
            "supermarket":   {"rate": 0.5,  "note": "0.5% cashback (base; supermarkets not in Chill Merchant list)",         "sort_key": 0.5},
            "transport":     {"rate": 0.5,  "note": "0.5% cashback (base rate)",                                             "sort_key": 0.5},
            "utilities":     {"rate": 0.5,  "note": "0.5% cashback (base rate)",                                             "sort_key": 0.5},
            "entertainment": {"rate": 10.0, "note": "Up to 10% at Chill Merchants — entertainment (World MC; HKD 1,500/month min)", "sort_key": 10.0},
            "overseas":      {"rate": 5.0,  "note": "5% cashback on overseas transactions (World MC); 4% Platinum MC",       "sort_key": 5.0},
            "general":       {"rate": 0.5,  "note": "0.5% cashback (base rate)",                                             "sort_key": 0.5},
            # Sub-categories
            "dining_fastfood":          {"rate": 10.0, "note": "Up to 10% at Chill Merchant fast food chains (World MC)",    "sort_key": 10.0},
            "entertainment_cinema":     {"rate": 10.0, "note": "Up to 10% at Chill Merchant cinemas (World MC)",             "sort_key": 10.0},
            "entertainment_streaming":  {"rate": 5.0,  "note": "5% cashback (streaming = online transaction)",               "sort_key": 5.0},
            "supermarket_hktvmall":     {"rate": 5.0,  "note": "5% cashback at HKTVmall (online transaction)",              "sort_key": 5.0},
            "overseas_japan":           {"rate": 5.0,  "note": "5% cashback on Japan/overseas (World MC)",                   "sort_key": 5.0},
        },
        "tip": "World MC: 10% at Chill Merchants (requires HKD 1,500/month), 5% online & overseas. Platinum MC: 8%/4% with HKD 1,000/month threshold. Also earns BOC Gift Points.",
        "cap_note": "10% Chill Merchant rate requires min. spend of HKD 1,500/month (World MC)",
    },

    # ── AEON ──────────────────────────────────────────────────────────────────
    "aeon_wakuwaku": {
        "name": "AEON CARD WAKUWAKU",
        "bank": "AEON",
        "reward_type": "cashback",
        "annual_fee": "Permanent waiver (no spend requirement)",
        "rewards": {
            "dining":        {"rate": 1.0,  "note": "1% WAKU COIN on local dining (F&B)",                              "sort_key": 1.0},
            "online":        {"rate": 6.0,  "note": "6% WAKU COIN on online spending (HKD 200 extra cap/month)",       "sort_key": 6.0},
            "travel":        {"rate": 6.0,  "note": "6% WAKU COIN on Japan & overseas travel (HKD 200 extra cap/month)", "sort_key": 6.0},
            "hotels":        {"rate": 6.0,  "note": "6% WAKU COIN on Japan & overseas hotels",                         "sort_key": 6.0},
            "supermarket":   {"rate": 0.4,  "note": "0.4% WAKU COIN (base rate; unlimited)",                           "sort_key": 0.4},
            "transport":     {"rate": 0.4,  "note": "0.4% WAKU COIN (base rate; unlimited)",                           "sort_key": 0.4},
            "utilities":     {"rate": 0.4,  "note": "0.4% WAKU COIN (base rate; unlimited)",                           "sort_key": 0.4},
            "entertainment": {"rate": 0.4,  "note": "0.4% WAKU COIN (base rate; unlimited)",                           "sort_key": 0.4},
            "overseas":      {"rate": 6.0,  "note": "6% WAKU COIN on all overseas/Japan spending (HKD 200 extra cap/month)", "sort_key": 6.0},
            "general":       {"rate": 0.4,  "note": "0.4% WAKU COIN (base rate; unlimited)",                           "sort_key": 0.4},
            # Sub-categories
            "overseas_japan":           {"rate": 6.0, "note": "6% WAKU COIN on Japan spending (AEON's headline benefit!)", "sort_key": 6.0},
            "supermarket_hktvmall":     {"rate": 6.0, "note": "6% WAKU COIN at HKTVmall (online transaction)",            "sort_key": 6.0},
            "entertainment_streaming":  {"rate": 6.0, "note": "6% WAKU COIN on streaming (online transaction)",           "sort_key": 6.0},
            "travel_klook":             {"rate": 6.0, "note": "6% WAKU COIN at Klook (online transaction)",               "sort_key": 6.0},
            "online_fashion":           {"rate": 6.0, "note": "6% WAKU COIN on fashion online",                           "sort_key": 6.0},
        },
        "tip": "6% WAKU COIN on online & Japan/overseas (HKD 200 extra/month cap); 1% local dining; 0.4% base unlimited. WAKU COIN = cash (10 coins = HKD 10). Permanent fee waiver.",
        "cap_note": "Extra WAKU COIN (above 0.4% base) capped at HKD 200/month combined",
        "no_fx_fee": True,
    },

    # ── DIGITAL BANKS ─────────────────────────────────────────────────────────
    "mox_credit": {
        "name": "Mox Credit Card",
        "bank": "Mox Bank",
        "reward_type": "cashback",
        "annual_fee": "Free",
        "rewards": {
            "dining":        {"rate": 1.0,  "note": "1% cashback (2% if Mox balance ≥ HKD 250k; no cap)", "sort_key": 1.0},
            "online":        {"rate": 1.0,  "note": "1% cashback (2% if Mox balance ≥ HKD 250k)",         "sort_key": 1.0},
            "travel":        {"rate": 1.0,  "note": "1% cashback",                                         "sort_key": 1.0},
            "hotels":        {"rate": 1.0,  "note": "1% cashback",                                         "sort_key": 1.0},
            "supermarket":   {"rate": 3.0,  "note": "3% cashback at supermarkets (no cap)",                "sort_key": 3.0},
            "transport":     {"rate": 1.0,  "note": "1% cashback",                                         "sort_key": 1.0},
            "utilities":     {"rate": 1.0,  "note": "1% cashback",                                         "sort_key": 1.0},
            "entertainment": {"rate": 1.0,  "note": "1% cashback",                                         "sort_key": 1.0},
            "overseas":      {"rate": 1.0,  "note": "1% cashback, zero FX fee",                            "sort_key": 1.0},
            "general":       {"rate": 1.0,  "note": "1% cashback on all spend (no cap)",                   "sort_key": 1.0},
            # Sub-categories
            "supermarket_parknshop":     {"rate": 3.0, "note": "3% cashback at PARKnSHOP/Circle K (supermarket)", "sort_key": 3.0},
            "supermarket_health_beauty": {"rate": 3.0, "note": "3% cashback at Mannings/Watsons/Sasa (supermarket MCC)", "sort_key": 3.0},
        },
        "tip": "3% cashback at supermarkets; 1% on everything else (upgrades to 2% with Mox savings balance ≥ HKD 250k). Zero FX fee. No annual fee, no cashback cap.",
        "no_fx_fee": True,
    },
    "za_card": {
        "name": "ZA Card",
        "bank": "ZA Bank",
        "reward_type": "cashback",
        "annual_fee": "Free",
        "rewards": {
            "dining":        {"rate": 1.0,  "note": "1% cashback guaranteed; PowerDraw may give random bonus", "sort_key": 1.0},
            "online":        {"rate": 1.0,  "note": "1% cashback guaranteed; PowerDraw may give random bonus", "sort_key": 1.0},
            "travel":        {"rate": 1.0,  "note": "1% cashback guaranteed",                                  "sort_key": 1.0},
            "hotels":        {"rate": 1.0,  "note": "1% cashback guaranteed",                                  "sort_key": 1.0},
            "supermarket":   {"rate": 1.0,  "note": "1% cashback guaranteed",                                  "sort_key": 1.0},
            "transport":     {"rate": 1.0,  "note": "1% cashback guaranteed",                                  "sort_key": 1.0},
            "utilities":     {"rate": 1.0,  "note": "1% cashback guaranteed",                                  "sort_key": 1.0},
            "entertainment": {"rate": 1.0,  "note": "1% cashback guaranteed",                                  "sort_key": 1.0},
            "overseas":      {"rate": 1.0,  "note": "1% cashback guaranteed",                                  "sort_key": 1.0},
            "general":       {"rate": 1.0,  "note": "1% cashback guaranteed on all eligible spend",            "sort_key": 1.0},
        },
        "tip": "Guaranteed 1% cashback on all spend. PowerDraw feature gives a chance at random bonus rebates (up to 200%). Fully digital, no annual fee.",
        "no_fx_fee": True,
    },

}  # end CARDS

# Grouped by bank for the Add Card flow
BANKS = {
    "HSBC":                   ["hsbc_red", "hsbc_visa_sig", "hsbc_everymile"],
    "Hang Seng":              ["hangseng_enjoy", "hangseng_mpower"],
    "Citi":                   ["citi_cashback", "citi_rewards", "citi_premiermiles"],
    "Standard Chartered":     ["sc_smart", "sc_cathay", "sc_simply_cash"],
    "sim":                    ["sim_credit", "sim_world_mc"],
    "DBS":                    ["dbs_black"],
    "BOC (Bank of China)":    ["boc_chill"],
    "AEON":                   ["aeon_wakuwaku"],
    "Digital Banks":          ["mox_credit", "za_card"],
}
