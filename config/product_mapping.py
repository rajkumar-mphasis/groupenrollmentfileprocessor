PRODUCT_MAPPING: dict[str, list[str]] = {
    # Critical Illness
    "CRIT": ["AG.CI.20.K.VOL", "AG.CI.21.H.VOL", "AG.CI.21.K.VOL", "AG.CI.28.H.VOL"],
    # Accident
    "ACCD": ["AG.AC.70.K.VOL", "AG.AC.77.H.VOL", "AG.AC.78.H.VOL"],
    # Hospital Indemnity
    "HIPL": ["AG.HI.80.K.VOL", "AG.HI.85R.H.VOL", "AG.HI.85.H.VOL", "AG.HI.88.H.VOL"],
    # Short Term Disability
    "STDI": ["AG.DI.50.K.VOL", "GLDASOSTD", "PLADSSTD", "GLDSTD", "STD"],
    # Long Term Disability
    "LTDI": ["GLDASOLTD", "PLADSLTD"],
    # Whole Life
    "LIFE": ["AG.WL.60.K.VOL"],
    # Term Life
    "TERM": [],
    # Cancer
    "CANC": [],
    # Dental
    "DENT": [],
    # Accident Employer Paid
    "ACER": ["AG.AC.70.K.EMP", "AG.AC.77.H.EMP", "AG.AC.78.H.EMP"],
    # Critical Illness Employer Paid
    "CIER": ["AG.CI.20.K.EMP", "AG.CI.21.H.EMP", "AG.CI.21.K.EMP", "AG.CI.28.H.EMP"],
    # Dental Employer Paid
    "DNER": [],
    # Short Term Disability Employer Paid
    "DIER": ["AG.DI.50.K.EMP"],
    # Hospital Indemnity Employer Paid
    "HIER": ["AG.HI.80.K.EMP", "AG.HI.85R.H.EMP", "AG.HI.85.H.EMP", "AG.HI.88.H.EMP"],
    # NY Hospital Indemnity
    "NYHI": ["AGNY.HI.80.K.VOL", "AGNY.HI.85.H.VOL"],
    # NY Critical Illness
    "NYCI": ["AGNY.CI.21.K.VOL", "AGNY.CI.28.H.VOL"],
    # NY Accident
    "NYAC": ["AGNY.AC.70.K.VOL", "AGNY.AC.77.H.VOL"],
    # NY Dental
    "NYDN": [],
    # NY Accident Employer Paid
    "NACR": ["AGNY.AC.70.K.EMP", "AGNY.AC.77.H.EMP"],
    # NY Critical Illness Employer Paid
    "NCIR": ["AGNY.CI.21.K.EMP", "AGNY.CI.28.H.EMP"],
    # NY Dental Employer Paid
    "NDNR": [],
    # NY Hospital Indemnity Employer Paid
    "NHIR": ["AGNY.HI.80.K.EMP", "AGNY.HI.85.H.EMP"],
    # Ben Extended Voluntary
    "BXVL": ["AG.HI.81.K.VOL"],
    # Ben Extended Employer Paid"
    "BXER": ["AG.HI.81.K.EMP"],
}
