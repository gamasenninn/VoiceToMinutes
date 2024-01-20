from pydub import AudioSegment
import numpy as np
import sys

def detect_silence(audio_file, silence_threshold=-50.0, chunk_size=10, silence_duration=2):
    """
    Detects silence in an audio file.

    :param audio_file: Path to the audio file
    :param silence_threshold: Silence threshold in dBFS
    :param chunk_size: Size of each chunk to analyze (in milliseconds)
    :param silence_duration: Minimum duration of silence to detect (in seconds)
    :return: List of tuples with the start and end time of each silence period
    """
    # Load audio file
    audio = AudioSegment.from_file(audio_file)

    # Convert silence threshold to amplitude
    silence_threshold = audio.dBFS + silence_threshold

    # Split audio into chunks
    chunks = np.array([chunk.dBFS for chunk in audio[::chunk_size]])

    # Detect silence
    silence = chunks < silence_threshold

    # Initialize variables
    start = None
    detected_silences = []

    for i, is_silent in enumerate(silence):
        # Check if current chunk is silent
        if is_silent and start is None:
            start = i * chunk_size

        # Check if current chunk is not silent and silence period was detected
        elif not is_silent and start is not None:
            end = i * chunk_size
            if (end - start) >= silence_duration * 1000:
                detected_silences.append((start, end))
            start = None

    # Check for silence at the end of the audio
    if start is not None:
        end = len(audio)
        if (end - start) >= silence_duration * 1000:
            detected_silences.append((start, end))

    return detected_silences

def format_time(milliseconds):
    """
    Converts milliseconds to a formatted time string (HH:MM:SS).
    """
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <audio_file_path>")
    else:
        audio_path = sys.argv[1]
        silences = detect_silence(audio_path)
        for start, end in silences:
            formatted_start = format_time(start)
            formatted_end = format_time(end)
            print(f"Silence from {formatted_start} - {formatted_end}")
