from presidio_analyzer import Pattern, PatternRecognizer

def build_regex_recognizers():
    recognizers = []

    email_pat = Pattern(name="email", regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", score=0.9)
    recognizers.append(PatternRecognizer(supported_entity="EMAIL_ADDRESS", patterns=[email_pat]))

    phone_pat = Pattern(name="phone", regex=r"\b(?:\+1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b", score=0.85)
    recognizers.append(PatternRecognizer(supported_entity="PHONE_NUMBER-R", patterns=[phone_pat]))
    # telefon regexi güçlendirilecek. aynı sayıda sayıların olduğu her şeyi phone kabul etmesin diye

    ssn_pat = Pattern(name="ssn", regex=r"\b\d{3}-\d{2}-\d{4}\b", score=0.9)
    recognizers.append(PatternRecognizer(supported_entity="US_SSN", patterns=[ssn_pat]))

    return recognizers
