# SRT-to-TextGrid
A Python program to convert SubRip Subtitle (.SRT) files to Praat-compatible TextGrid files, with support for batch conversion and individual file conversion. Ideal for linguists and researchers working with speech data and transcription alignment.

Paste in CMD: Pip install pysrt


How to use convert_single_srt_to_textgrid:

1. SRT file needs to be in the same folder as the Python Script.
2. The TextGrid file will be outputted in the same folder as the script.

How to use batch_convert_srt_to_textgrid:

1. Input the directory path of .srt files you want to convert
2. All converted files will be outputted in the same directory


How to use batch_convert_srt_to_textgrid_diff_directory:

1. Input the directory path of .srt files and the output path where you want the converted files to go to.
2. Make sure the output folder exists before running the program.
