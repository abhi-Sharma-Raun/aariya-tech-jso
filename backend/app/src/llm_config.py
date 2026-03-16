from langchain_groq import ChatGroq
import assemblyai as aai
from ..config import settings

llm=ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.01,
    max_retries=3,
    api_key=f"{settings.groq_api_key}"
)

aai.settings.api_key = f"{settings.assemblyai_api_key}"
config = aai.TranscriptionConfig(
    speech_models=["universal-2"], language_code="en", speaker_labels=True,
    speech_understanding= aai.SpeechUnderstandingRequest(
        request= aai.SpeechUnderstandingFeatureRequests(
            speaker_identification= aai.SpeakerIdentificationRequest(
                speaker_type= "role",
                known_values= ["Interviewer", "Interviewee"]
            )))
    )

def transcribe_audio_file(audio_url: str, config: aai.TranscriptionConfig=config):
    transcript = aai.Transcriber(config=config).transcribe(audio_url)
    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return transcript.utterances if transcript.utterances else transcript.text