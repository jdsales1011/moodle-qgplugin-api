# ERROR RESPONSE
data = {
    "status" : "error",
    "error" : {
        "code" : 400,
        "message" : "Invalid request data",
    }
}

# IDENTIFICATION
data = {
    "status": "success",
    "questions": [
        {
            "id": 1,
            "question": "Zaphod Beeblebrox?",
            "answer": "Betelgeusian"
        },
        {
            "id": 2,
            "question": "Zaphod Beeblebrox?",
            "answer": "Betelgeusian"
        }
    ]
}

# TRUE OR FALSE
data = {
    "status": "success",
    "questions": [
        {
            "question": "Zaphod Beeblebrox",
            "answer": True
        },
        {
            "question": "Zaphod Beeblebrox",
            "answer": False
        }
    ]
}

# MULTIPLE CHOICE
data = {
    "status": "success",
    "questions": [
        {
            "question": "Zaphod Beeblebrox?",
            "choices": "[A. A cross, B. A bell, C. A golden statue of the Virgin Mary, D. A flag]",
            "answer": 'D'
        },
        {
            "question": "Zaphod Beeblebrox?",
            "choices": "[A. A cross, B. A bell, C. A golden statue of the Virgin Mary, D. A flag]",
            "answer": 'D'
        }
    ]
}