#TODO JUANFER inventoryHTML(inventory)
def inventoryHTML(inventory: dict) -> str:
    return f"<body>{inventory}</body>"

def OTPHTML(num: int) -> str:
    return f"<body> OTP :{num} </body>"
def maintenanceHTML(maintenance: dict) -> str:
    return f"<body>{str(maintenance)}</body>"