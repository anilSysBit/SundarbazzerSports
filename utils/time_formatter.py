def format_duration(duration):
    # Extract total seconds from timedelta
    total_seconds = int(duration.total_seconds())
    
    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Construct the human-readable format
    result = []
    if hours:
        result.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes:
        result.append(f"{minutes} min")
    if seconds:
        result.append(f"{seconds} sec")

    return ' '.join(result)