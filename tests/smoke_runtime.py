"""Optional full-dependency smoke test; never downloads model weights."""
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HOME"] = str(ROOT / ".cache/huggingface")
sys.path.insert(0, str(ROOT / "app"))

import torch
import torchaudio
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from chatterbox.tts_turbo import ChatterboxTurboTTS
from gradio_client import Client
import app as tts

with tempfile.TemporaryDirectory() as directory:
    tts.output_dir = Path(directory)
    path = tts.save_audio(torch.zeros(1, 2400), 24000, "smoke.wav", "turbo")
    audio, sr = torchaudio.load(path)
    assert sr == 24000 and audio.shape == (1, 2400)

try:
    _, url, _ = tts.app.launch(server_name="127.0.0.1", prevent_thread_lock=True,
                             theme=tts.gr.themes.Soft(), css=tts.css)
    client = Client(url, verbose=False)
    result = client.predict(next(iter(tts.MODEL_CHOICES)), "", None,
                            .5, .5, .8, .05, .95, 1.2, 1000, True, "en", "",
                            api_name="/generate_speech")
    assert result[0] is None and "Please enter some text" in result[1], result
    print("PASS: model imports, WAV round-trip, Gradio launch and queued API request")
finally:
    tts.app.close()
