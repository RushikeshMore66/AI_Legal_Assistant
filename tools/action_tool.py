def suggest_actions(intent):
    actions_map = {
        "criminal": [
            "File FIR at nearest police station",
            "Collect evidence",
            "Consult criminal lawyer"
        ],
        "cyber": [
            "Report on cybercrime.gov.in",
            "Preserve screenshots",
            "File complaint under IT Act"
        ],
        "employment": [
            "Contact labour commissioner",
            "Send legal notice",
            "File complaint in labour court"
        ],
        "consumer": [
            "File complaint on consumer forum",
            "Keep receipts",
            "Send formal notice"
        ]
    }

    return actions_map.get(intent, ["Consult legal expert"])