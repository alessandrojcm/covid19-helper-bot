# Here are common twilio actions used by several files

screening_not_in_danger = {
    "actions": [
        {
            "say": """Great! Then you probably do't have anything to worry about!
                                  Feel free to run the test again if you want"""
        },
        {"redirect": "task://menu-description"},
    ]
}

screening_pre_results_warning = [
    {
        "say": """
               Please bear in mind that this tool is merely informative.
               If, after all, you don't feel ill there should not be any cause for alarm
               """
    },
    {"redirect": "task://menu-description"},
]
