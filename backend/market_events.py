MARKET_EVENTS = [
    {
        "id": "gfc",
        "title": "Global Financial Crisis",
        "image": "assets/market_events/gfc.webp",
        "description": "Triggered by the US Subprime mortgage collapse. In India, foreign investors pulled out billions overnight. The Sensex saw 'Lower Circuits' (trading halts) as panic peaked.",
        "recovery": "The V-Shape: Within a year, massive government stimulus and low interest rates sparked a rally. Those who didn't panic-sell saw their portfolios bounce back by 25%+.",
        "movements": "Equity: Sensex fell ~52% in 1 year. Rupee: Depreciated to 50/$1. Gold: Remained stable/up as a safe haven while FIIs pulled out massive liquidity.",
        "impact": {"Equity": -0.52, "Debt": -0.07, "Gold": 0.05, "Silver": -0.10, "Oil": -0.15, "Cash": 0.04},
        "stabilization": {"Equity": 0.35, "Debt": 0.08, "Gold": 0.05, "Silver": 0.15, "Oil": 0.10, "Cash": -0.02}
    },
    {
        "id": "rate_shock",
        "title": "Interest Rate Shock",
        "image": "assets/market_events/rate_shock.webp",
        "description": "The Fed's 'Taper Tantrum' caused the Rupee to 'fall off a cliff.' India was labeled part of the 'Fragile Five' economies. Debt yields spiked, causing bond prices to crash.",
        "recovery": "Stabilization: The RBI hiked rates aggressively to save the Rupee. A year later, inflation cooled, and the Debt market stabilized as foreign confidence returned.",
        "movements": "Debt: Bond yields spiked; prices crashed. Rupee: Hit record lows (₹68/$1). Equity: Mid/Small caps hit harder than Large caps due to borrowing costs.",
        "impact": {"Equity": -0.15, "Debt": -0.18, "Gold": -0.05, "Silver": -0.10, "Oil": -0.06, "Cash": 0.06},
        "stabilization": {"Equity": 0.12, "Debt": 0.10, "Gold": 0.03, "Silver": 0.05, "Oil": 0.04, "Cash": 0.02}
    },
    {
        "id": "inflation_shock",
        "title": "Inflation Shock",
        "image": "assets/market_events/inflation.webp",
        "description": "Double-digit inflation led to 'Negative Real Interest Rates'—meaning money in the bank was losing value. Gold prices hit record highs as Indians rushed for 'Physical Safety.'",
        "recovery": "Mean Reversion: High rates eventually crushed demand. As inflation dipped below 6%, Equity and Debt began to outperform Gold again as the 'Risk-On' sentiment returned.",
        "movements": "Cash: Real returns became negative (Inflation > Savings Rate). Gold: Prices surged as it was the only asset beating WPI inflation of 9.5%. Equity: Flat/Negative.",
        "impact": {"Equity": -0.10, "Debt": -0.08, "Gold": 0.25, "Silver": 0.15, "Oil": 0.05, "Cash": -0.07},
        "stabilization": {"Equity": 0.15, "Debt": 0.12, "Gold": -0.05, "Silver": -0.05, "Oil": 0.02, "Cash": 0.03}
    },
    {
        "id": "commodity_shock",
        "title": "Oil & Commodity Shock",
        "image": "assets/market_events/commodity.webp",
        "description": "As a nation that imports 80% of its oil, a spike to $120/barrel creates a 'Twin Deficit' crisis. Transportation costs soar, hurting every manufacturing company in India.",
        "recovery": "Efficiency Gains: Companies optimized supply chains. As global supply normalized, oil prices cooled, leading to a massive 'margin expansion' and a rally in Auto/Logistics stocks.",
        "movements": "Oil: Brent Crude crossed $120. Equity: Margin pressure on Auto, Paints, and Airlines (high input costs). Silver: Surged along with industrial commodities.",
        "impact": {"Equity": -0.18, "Debt": -0.05, "Gold": 0.05, "Silver": 0.15, "Oil": 0.45, "Cash": -0.03},
        "stabilization": {"Equity": 0.22, "Debt": 0.05, "Gold": -0.02, "Silver": -0.10, "Oil": -0.15, "Cash": 0.02}
    },
    {
        "id": "liquidity_shock",
        "title": "Domestic Liquidity Shock",
        "image": "assets/market_events/liquidity.webp",
        "description": "Overnight, 86% of cash was 'invalid.' The informal economy, which runs on cash, ground to a halt. Real Estate transactions vanished, and retail consumption dropped 40%.",
        "recovery": "Digital Revolution: While the initial shock was painful, it led to the explosion of UPI and digital payments. A year later, the formal economy emerged stronger and more transparent.",
        "movements": "Cash: Massive 'Physical Cash' shortage. Equity: Realty and Luxury stocks crashed 15-20% in days. Debt: Banks became flush with funds; FD rates started falling.",
        "impact": {"Equity": -0.20, "Debt": 0.05, "Gold": 0.02, "Silver": 0.05, "Oil": 0.01, "Cash": 0.50},
        "stabilization": {"Equity": 0.35, "Debt": 0.03, "Gold": 0.05, "Silver": -0.02, "Oil": 0.02, "Cash": -0.15}
    },
    {
        "id": "credit_crisis",
        "title": "Shadow Banking Crisis",
        "image": "assets/market_events/credit.webp",
        "description": "The 'Lehman moment' for Indian NBFCs. When IL&FS defaulted, the 'Trust Deficit' meant even good companies couldn't borrow money. Mutual funds faced massive exit pressures.",
        "recovery": "Flight to Quality: The crisis weeded out weak players. Investors moved money to 'AAA' rated banks and blue-chip companies, which saw their market share grow significantly.",
        "movements": "Debt: Mutual Fund 'Credit Risk' funds saw 10-20% NAV drops. Equity: NBFC stocks crashed 40-60%. Gold: Steady.",
        "impact": {"Equity": -0.25, "Debt": -0.20, "Gold": 0.02, "Silver": 0.02, "Oil": 0.01, "Cash": 0.10},
        "stabilization": {"Equity": 0.30, "Debt": 0.15, "Gold": 0.05, "Silver": 0.05, "Oil": 0.01, "Cash": -0.05}
    },
    {
        "id": "pandemic",
        "title": "Pandemic / Black Swan",
        "image": "assets/market_events/pandemic.webp",
        "description": "A 'forced' economic stop. Markets crashed 30% in weeks. However, Technology and Pharma sectors became the new market leaders as the world went digital/health-first.",
        "recovery": "The Great Rebound: Unprecedented global liquidity created the 'Mother of all Bull Markets.' Asset classes like Silver and Tech-Equities saw 50-100% returns within 12 months.",
        "movements": "Equity: Nifty fell 38% in 30 days. Gold/Silver: Initially fell (liquidity hunt), then rallied 25%+ within 6 months. Cash: Increased in demand.",
        "impact": {"Equity": -0.38, "Debt": -0.05, "Gold": 0.15, "Silver": 0.25, "Oil": -0.40, "Cash": 0.12},
        "stabilization": {"Equity": 0.60, "Debt": 0.06, "Gold": 0.10, "Silver": 0.40, "Oil": 0.30, "Cash": -0.05}
    },
    {
        "id": "war_shock",
        "title": "Geopolitical War Shock",
        "image": "assets/market_events/war.webp",
        "description": "War in Europe or the Middle East disrupts the 'Energy Map.' Investors move to 'War Hedges' like Gold and Crude Oil. Equities are sold to raise 'War Chest' cash.",
        "recovery": "Normalcy Premium: Once the conflict localized or a stalemate was reached, markets 'priced in' the war. Equities recovered as global trade routes found expensive but workable alternatives.",
        "movements": "Oil: Spikes instantly. Gold: Prices rise on 'War Premium.' Equity: Defensive sectors (IT/Pharma) held better than cyclical ones (Banks/Steel).",
        "impact": {"Equity": -0.15, "Debt": -0.02, "Gold": 0.20, "Silver": 0.10, "Oil": 0.35, "Cash": 0.06},
        "stabilization": {"Equity": 0.18, "Debt": 0.04, "Gold": -0.05, "Silver": -0.03, "Oil": -0.10, "Cash": -0.02}
    },
    {
        "id": "currency_flight",
        "title": "Currency Flight Crisis",
        "image": "assets/market_events/currency.webp",
        "description": "A 'Run on the Rupee.' When forex reserves dwindled to just 3 weeks of imports, the government had to air-lift gold to London as collateral. Total economic uncertainty.",
        "recovery": "Reform Rally: The crisis forced India to open its markets (1991 Liberalization). What started as a collapse ended in the greatest wealth-creation era in Indian history.",
        "movements": "Rupee: Devalued by ~18-20% against the USD. Equity: High uncertainty initially; then massive 'Post-Reform' rally as markets opened up.",
        "impact": {"Equity": -0.30, "Debt": -0.15, "Gold": 0.10, "Silver": 0.05, "Oil": 0.15, "Cash": -0.10},
        "stabilization": {"Equity": 0.50, "Debt": 0.10, "Gold": 0.05, "Silver": 0.02, "Oil": 0.01, "Cash": 0.05}
    },
    {
        "id": "bubble_burst",
        "title": "Asset Bubble Burst",
        "image": "assets/market_events/bubble.webp",
        "description": "'Irrational Exuberance.' Whether it was the 1992 Scam or 2000 Tech bubble, valuations lost touch with reality. When the music stopped, there were no buyers.",
        "recovery": "The Long Grind: Unlike other shocks, bubbles take longer to heal. It took years for the 'junk' stocks to vanish, while quality companies with real profits eventually led the new cycle.",
        "movements": "Equity: Specifically 'High-Flying' Scam/Tech stocks fell 80-90%. Debt/Cash: Became the only way to preserve capital as the bubble popped.",
        "impact": {"Equity": -0.45, "Debt": 0.05, "Gold": -0.10, "Silver": -0.20, "Oil": -0.05, "Cash": 0.06},
        "stabilization": {"Equity": 0.20, "Debt": 0.03, "Gold": 0.10, "Silver": 0.15, "Oil": 0.05, "Cash": -0.02}
    },

    {
        "id": "cyber_attack",
        "title": "Major Cyber Attack",
        "image": "assets/market_events/cyber.webp",
        "description": "A massive ransomware attack hits the NSE servers and major private banks, freezing trading for 48 hours and causing panic regarding digital wealth safety.",
        "recovery": "Digital Fortification: Government announces a new Cybersecurity Law. Confidence returns as banks confirm zero data loss, leading to a tech-driven recovery.",
        "movements": "Equity: Tech and Bank stocks tank. Cash: Massive demand for physical currency. Gold: Spikes as people distrust digital systems.",
        "impact": {"Equity": -0.15, "Debt": -0.05, "Gold": 0.08, "Silver": 0.04, "Oil": -0.02, "Cash": 0.10},
        "stabilization": {"Equity": 0.12, "Debt": 0.03, "Gold": -0.04, "Silver": -0.02, "Oil": 0.01, "Cash": -0.08}
    },
    {
        "id": "natural_disaster",
        "title": "Extreme Monsoon/Floods",
        "image": "assets/market_events/flood.webp",
        "description": "Unprecedented nationwide flooding destroys 30% of the Kharif crop. Food inflation skyrockets, and supply chains for auto/manufacturing are broken.",
        "recovery": "Rural Stimulus: Government announces farm loan waivers and infrastructure spending, boosting cement and rural consumption stocks.",
        "movements": "Oil: Prices rise due to transport blocks. Equity: FMCG and Auto take a hit. Gold: Farmers sell gold to survive, stabilizing prices.",
        "impact": {"Equity": -0.10, "Debt": -0.02, "Gold": 0.02, "Silver": 0.01, "Oil": 0.12, "Cash": 0.05},
        "stabilization": {"Equity": 0.08, "Debt": 0.04, "Gold": 0.02, "Silver": 0.01, "Oil": -0.05, "Cash": -0.03}
    },
    {
        "id": "political_instability",
        "title": "Coalition Collapse",
        "image": "assets/market_events/politics.webp",
        "description": "A surprise collapse of the central government leads to an unscheduled election. Markets fear the reversal of major economic reforms.",
        "recovery": "Democratic Resolve: A stable majority is elected 3 months later. Markets rally on the return of 'Policy Certainty'.",
        "movements": "Equity: Sharp drop on uncertainty. Rupee: Weakens as FIIs wait for election results. Debt: Bond yields spike.",
        "impact": {"Equity": -0.20, "Debt": -0.08, "Gold": 0.06, "Silver": 0.03, "Oil": -0.05, "Cash": 0.04},
        "stabilization": {"Equity": 0.22, "Debt": 0.06, "Gold": -0.02, "Silver": -0.01, "Oil": 0.03, "Cash": -0.02}
    },
    {
        "id": "taper_tantrum_2",
        "title": "The New Taper Tantrum",
        "image": "assets/market_events/taper.webp",
        "description": "The US Fed hikes rates faster than expected. Foreign investors pull out of 'Emerging Markets' like India to chase higher yields in the US Dollar.",
        "recovery": "RBI Intervention: The RBI aggressively uses Forex reserves to defend the Rupee and hikes domestic rates to attract capital back.",
        "movements": "Debt: Bond prices crash as yields rise. Equity: Mid-caps hit hardest. Cash: High-interest savings look attractive.",
        "impact": {"Equity": -0.18, "Debt": -0.12, "Gold": -0.05, "Silver": -0.06, "Oil": -0.10, "Cash": 0.08},
        "stabilization": {"Equity": 0.15, "Debt": 0.10, "Gold": 0.04, "Silver": 0.03, "Oil": 0.05, "Cash": -0.04}
    }
]
