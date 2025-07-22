import pysrt

def srt_to_textgrid(srt_file, textgrid_file):
    """
    Convert an SRT file to a TextGrid file with two structured tiers: Interviewer and Participant.
    Ensures that each dialogue has a start and end boundary.
    
    Args:
        srt_file (str): Path to the input .srt file.
        textgrid_file (str): Path to the output .TextGrid file.
    """
    subs = pysrt.open(srt_file)

    # Determine the maximum time
    max_time = max(sub.end.ordinal / 1000.0 for sub in subs)

    # Separate subtitles into Interviewer and Participant tiers
    interviewer_intervals = []
    participant_intervals = []

    last_end_time_interviewer = 0.0
    last_end_time_participant = 0.0

    for sub in subs:
        text = sub.text.replace("\n", " ").replace("\"", "\"\"")  # Handle newlines and escape quotes
        start_time = sub.start.ordinal / 1000.0
        end_time = sub.end.ordinal / 1000.0

        if "Interviewer" in text:
            # If there is a gap from the last dialogue, insert an empty interval
            if start_time > last_end_time_interviewer:
                interviewer_intervals.append((last_end_time_interviewer, start_time, ""))

            # Add actual dialogue
            interviewer_intervals.append((start_time, end_time, text))
            last_end_time_interviewer = end_time
        else:
            # If there is a gap from the last dialogue, insert an empty interval
            if start_time > last_end_time_participant:
                participant_intervals.append((last_end_time_participant, start_time, ""))

            # Add actual dialogue
            participant_intervals.append((start_time, end_time, text))
            last_end_time_participant = end_time

    # Ensure that the tiers extend to max_time
    if last_end_time_interviewer < max_time:
        interviewer_intervals.append((last_end_time_interviewer, max_time, ""))
    if last_end_time_participant < max_time:
        participant_intervals.append((last_end_time_participant, max_time, ""))

    # Start writing the TextGrid file
    with open(textgrid_file, 'w', encoding='utf-8') as f:
        f.write("File type = \"ooTextFile\"\n")
        f.write("Object class = \"TextGrid\"\n\n")
        f.write(f"xmin = 0.0\n")
        f.write(f"xmax = {max_time:.6f}\n")
        f.write("tiers? <exists>\n")
        f.write("size = 2\n")  # Two tiers: Interviewer and Participant
        f.write("item []:\n")

        # Write Interviewer Tier
        f.write("    item [1]:\n")
        f.write("        class = \"IntervalTier\"\n")
        f.write("        name = \"Interviewer\"\n")
        f.write(f"        xmin = 0.0\n")
        f.write(f"        xmax = {max_time:.6f}\n")
        f.write(f"        intervals: size = {len(interviewer_intervals)}\n")

        for i, (start_time, end_time, text) in enumerate(interviewer_intervals, start=1):
            f.write(f"        intervals [{i}]:\n")
            f.write(f"            xmin = {start_time:.6f}\n")
            f.write(f"            xmax = {end_time:.6f}\n")
            f.write(f"            text = \"{text}\"\n")

        # Write Participant Tier
        f.write("    item [2]:\n")
        f.write("        class = \"IntervalTier\"\n")
        f.write("        name = \"Participant\"\n")
        f.write(f"        xmin = 0.0\n")
        f.write(f"        xmax = {max_time:.6f}\n")
        f.write(f"        intervals: size = {len(participant_intervals)}\n")

        for i, (start_time, end_time, text) in enumerate(participant_intervals, start=1):
            f.write(f"        intervals [{i}]:\n")
            f.write(f"            xmin = {start_time:.6f}\n")
            f.write(f"            xmax = {end_time:.6f}\n")
            f.write(f"            text = \"{text}\"\n")

    print(f"Conversion complete: {textgrid_file}")

# Example Usage:
srt_file = "ESP2_S1_deidentified_test.srt"  # Replace with your actual SRT file
textgrid_file = "ESP2_S1_deidentified_test.TextGrid"  # Output file
srt_to_textgrid(srt_file, textgrid_file)
