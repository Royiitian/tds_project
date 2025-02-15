import whisper

def convert_audio_to_text(audio_file):
    # Load Whisper model (options: "tiny", "base", "small", "medium", "large")
    model = whisper.load_model("base")  # Change model size if needed

    # Transcribe audio
    #result = model.transcribe("your-audio-file.mp3")
    result = model.transcribe("/data/Sports.mp3")

    # Print the transcribed text
    print("Transcription:", result["text"])