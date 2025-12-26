from urllib.parse import quote


def find_therapists(location: str) -> str:
    """Generate Psychology Today search link for therapists near the location."""
    
    encoded_location = quote(location)
    psychology_today_url = f"https://www.psychologytoday.com/us/therapists?search={encoded_location}"
    
    return (
        f"Find therapists near {location}:\n\n"
        f"Psychology Today Directory:\n{psychology_today_url}\n\n"
        "This directory shows verified therapists with:\n"
        "- Name, photo, and credentials\n"
        "- Phone number and email\n"
        "- Specialties and insurance accepted\n"
        "- Reviews and availability\n\n"
        "Tip: Filter by insurance, specialty, and availability to find your best match."
    )