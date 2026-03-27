def generate_complaint(details: str, authority="Concerned Authority"):
    return f"""
    FORMAL COMPLAINT

    To,
    {authority}

    Subject: Complaint regarding issue

    Dear Sir/Madam,

    I am writing to bring to your attention the following issue:

    {details}

    Kindly take appropriate action at the earliest.

    Sincerely,
    [Your Name]
    """