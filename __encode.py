def encode(name, upper=True) -> str:
    from unicodedata import normalize

    ascii_name = normalize("NFKD", name).encode("ascii", errors="ignore").decode("ascii")        
    return ascii_name.upper() if upper else ascii_name