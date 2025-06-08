import gradio as gr
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import devicetorch
import torch
import os
import tempfile
import time
from pathlib import Path

# Initialize output directory
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Get the appropriate device
device = devicetorch.get(torch)
print(f"Using device: {device}")

# Load the Chatterbox TTS model
print("Loading Chatterbox TTS model...")
try:
    model = ChatterboxTTS.from_pretrained(device=device)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

def generate_speech(text, reference_audio, exaggeration, cfg_value, output_filename):
    """Generate speech using Chatterbox TTS"""
    if model is None:
        return None, "❌ Model not loaded. Please check the installation."
    
    if not text or not text.strip():
        return None, "❌ Please enter some text to convert to speech."
    
    try:
        print(f"Generating speech for: {text[:50]}...")
        
        # Prepare parameters
        params = {
            "exaggeration": exaggeration,
            "cfg_weight": cfg_value
        }
        
        # Add reference audio if provided
        if reference_audio is not None:
            params["audio_prompt_path"] = reference_audio
            print(f"Using voice cloning with reference audio: {reference_audio}")
        
        # Generate speech
        wav = model.generate(text, **params)
        
        # Create output filename
        if not output_filename:
            timestamp = int(time.time())
            output_filename = f"chatterbox_output_{timestamp}.wav"
        
        if not output_filename.endswith('.wav'):
            output_filename += '.wav'
        
        # Save to outputs directory
        output_path = output_dir / output_filename
        ta.save(str(output_path), wav, model.sr)
        
        print(f"✅ Speech generated successfully: {output_path}")
        return str(output_path), f"✅ Speech generated successfully!\nSaved as: {output_filename}"
        
    except Exception as e:
        error_msg = f"❌ Error generating speech: {str(e)}"
        print(error_msg)
        return None, error_msg

def get_audio_info(audio_file):
    """Get information about uploaded audio file"""
    if audio_file is None:
        return "No audio file uploaded"
    
    try:
        # Load audio to get info
        waveform, sample_rate = ta.load(audio_file)
        duration = waveform.shape[1] / sample_rate
        channels = waveform.shape[0]
        
        return f"📊 Audio Info:\n• Duration: {duration:.2f} seconds\n• Sample Rate: {sample_rate} Hz\n• Channels: {channels}\n• Recommended: 10+ seconds, 24kHz+, mono"
    except Exception as e:
        return f"❌ Error reading audio: {str(e)}"

# Create the Gradio interface
with gr.Blocks(
    title="Chatterbox TTS",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background: #f9f9f9;
    }
    """
) as app:
    
    with gr.Row():
        gr.Markdown(
            """
            # 🎙️ Chatterbox TTS
            ### AI-Powered Text-to-Speech with Voice Cloning
            
            Generate natural-sounding speech from text with optional voice cloning capabilities.
            """,
            elem_classes=["main-header"]
        )
    
    with gr.Tabs():
        # Main TTS Tab
        with gr.TabItem("🎤 Text-to-Speech"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📝 Input Text")
                    text_input = gr.Textbox(
                        label="Text to Convert",
                        placeholder="Enter the text you want to convert to speech...",
                        lines=5,
                        max_lines=10
                    )
                    
                    gr.Markdown("### 🎨 Voice Settings")
                    with gr.Row():
                        exaggeration = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.5,
                            step=0.1,
                            label="Emotion Exaggeration",
                            info="Higher values make speech more expressive"
                        )
                        cfg_value = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.5,
                            step=0.1,
                            label="CFG Scale",
                            info="Lower values = slower, more deliberate speech"
                        )
                    
                    output_filename = gr.Textbox(
                        label="Output Filename (optional)",
                        placeholder="my_speech.wav",
                        info="Leave empty for auto-generated name"
                    )
                    
                    generate_btn = gr.Button(
                        "🎵 Generate Speech",
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 🎯 Voice Cloning (Optional)")
                    reference_audio = gr.Audio(
                    label="Reference Audio for Voice Cloning (Upload 10+ seconds of clear speech)",
                    type="filepath"
                    )
                    
                    audio_info = gr.Textbox(
                        label="Audio Information",
                        interactive=False,
                        max_lines=5
                    )
                    
                    gr.Markdown("### 🔊 Generated Output")
                    output_audio = gr.Audio(
                        label="Generated Speech",
                        type="filepath"
                    )
                    
                    status_output = gr.Textbox(
                        label="Status",
                        interactive=False,
                        max_lines=3
                    )
        
        # Examples Tab
        with gr.TabItem("📚 Examples & Tips"):
            gr.Markdown("""
            ## 🎯 Voice Cloning Tips
            
            ### For Best Results:
            - **Duration**: Use at least 10 seconds of reference audio
            - **Quality**: Clear speech, no background noise
            - **Format**: WAV format preferred, 24kHz+ sample rate
            - **Content**: Single speaker, natural speaking style
            - **Microphone**: Professional microphone recommended
            
            ### Example Texts:
            - "Hello, this is a test of the Chatterbox text-to-speech system."
            - "The quick brown fox jumps over the lazy dog."
            - "Welcome to our AI-powered voice synthesis demonstration."
            
            ### Emotion Control:
            - **Low exaggeration (0.0-0.3)**: Calm, professional tone
            - **Medium exaggeration (0.4-0.6)**: Natural, conversational
            - **High exaggeration (0.7-1.0)**: Expressive, dramatic
            
            ### CFG Scale:
            - **Low CFG (0.0-0.3)**: Slower, more deliberate speech
            - **Medium CFG (0.4-0.6)**: Balanced pacing
            - **High CFG (0.7-1.0)**: Faster, more natural rhythm
            """)
        
        # About Tab
        with gr.TabItem("ℹ️ About"):
            gr.Markdown(f"""
            ## About Chatterbox TTS
            
            **Chatterbox** is an open-source text-to-speech model developed by Resemble AI.
            
            ### Features:
            - 🎭 **Voice Cloning**: Clone any voice with just 10 seconds of audio
            - 🎨 **Emotion Control**: Adjust expressiveness and pacing
            - 🆓 **Free & Open Source**: MIT license, completely free to use
            - 🔒 **Privacy**: Runs completely locally on your machine
            - 🌐 **Cross-Platform**: Works on Windows, Mac, and Linux
            
            ### Technical Details:
            - **Device**: {device}
            - **Model**: Chatterbox TTS (Resemble AI)
            - **Output Format**: WAV audio files
            - **Sample Rate**: Variable (model default)
            
            ### Credits:
            - **Chatterbox TTS**: Resemble AI
            - **Integration**: Pinokio Community
            - **Interface**: Gradio
            
            For more information, visit: [Resemble AI](https://www.resemble.ai/)
            """)
    
    # Event handlers
    reference_audio.change(
        fn=get_audio_info,
        inputs=[reference_audio],
        outputs=[audio_info]
    )
    
    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, reference_audio, exaggeration, cfg_value, output_filename],
        outputs=[output_audio, status_output]
    )

# Launch the application
if __name__ == "__main__":
    print(f"\n🚀 Starting Chatterbox TTS on device: {device}")
    print("🌐 The application will be available in your web browser")
    
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False
    ) 