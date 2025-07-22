import os
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
            if start_time > last_end_time_interviewer:
                interviewer_intervals.append((last_end_time_interviewer, start_time, ""))

            interviewer_intervals.append((start_time, end_time, text))
            last_end_time_interviewer = end_time
        else:
            if start_time > last_end_time_participant:
                participant_intervals.append((last_end_time_participant, start_time, ""))

            participant_intervals.append((start_time, end_time, text))
            last_end_time_participant = end_time

    if last_end_time_interviewer < max_time:
        interviewer_intervals.append((last_end_time_interviewer, max_time, ""))
    if last_end_time_participant < max_time:
        participant_intervals.append((last_end_time_participant, max_time, ""))

    # Ensure output directory exists
    os.makedirs(os.path.dirname(textgrid_file), exist_ok=True)

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

    print(f"Yay! Converted: {srt_file} → {textgrid_file}")

def batch_convert_srt_to_textgrid(input_dir, output_dir):
    """
    Finds all .srt files in a given input directory and converts them to .TextGrid files in an output directory.

    Args:
        input_dir (str): The directory containing .srt files.
        output_dir (str): The directory where .TextGrid files will be saved.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    srt_files = [f for f in os.listdir(input_dir) if f.endswith(".srt")]

    if not srt_files:
        print(f"Uh oh! No SRT files found in {input_dir}.")
        return

    for srt_file in srt_files:
        srt_path = os.path.join(input_dir, srt_file)
        textgrid_file = os.path.join(output_dir, srt_file.replace(".srt", ".TextGrid"))

        srt_to_textgrid(srt_path, textgrid_file)

# Run the batch conversion with specified directories
if __name__ == "__main__":
    input_directory = r"D:\Jupyter Notebook\Srt Test Folder"  # Change this to your SRT input folder
    output_directory = r"D:\Jupyter Notebook\TextGrid Output"  # Change this to your output folder
    batch_convert_srt_to_textgrid(input_directory, output_directory)
