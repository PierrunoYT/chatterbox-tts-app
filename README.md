# 🎙️ Chatterbox TTS App

AI-Powered Text-to-Speech with Voice Cloning using Chatterbox TTS and Gradio interface.

## ✨ Features

- 🎭 **Voice Cloning**: Clone any voice with just 10 seconds of audio
- 🎨 **Emotion Control**: Adjust expressiveness and pacing
- 🆓 **Free & Open Source**: MIT license, completely free to use
- 🔒 **Privacy**: Runs completely locally on your machine
- 🌐 **Cross-Platform**: Works on Windows, Mac, and Linux
- 🖥️ **Web Interface**: Easy-to-use Gradio interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended) or CPU

### Installation

1. Clone this repository:
```bash
git clone https://github.com/PierrunoYT/chatterbox-tts-app.git
cd chatterbox-tts-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://127.0.0.1:7860`

## 🎯 Usage

### Basic Text-to-Speech
1. Enter your text in the input field
2. Adjust emotion and CFG settings as desired
3. Click "Generate Speech"
4. Download your generated audio

### Voice Cloning
1. Upload a reference audio file (10+ seconds recommended)
2. Enter your text
3. Adjust settings
4. Generate speech with the cloned voice

## 🎨 Settings

- **Emotion Exaggeration**: Controls how expressive the speech is (0.0 = calm, 1.0 = very expressive)
- **CFG Scale**: Controls speech pacing (0.0 = slower/deliberate, 1.0 = faster/natural)

## 📁 Project Structure

```
chatterbox-tts-app/
├── app.py              # Main Gradio application
├── requirements.txt    # Python dependencies
├── outputs/           # Generated audio files (created automatically)
├── icon.png           # Application icon
└── pinokio files/     # Pinokio integration files
```

## 🔧 Technical Details

- **Model**: Chatterbox TTS by Resemble AI
- **Interface**: Gradio web interface
- **Audio Format**: WAV files
- **Device Support**: CUDA GPU / CPU automatic detection

## 📝 Tips for Best Results

### Voice Cloning
- Use at least 10 seconds of clear reference audio
- Ensure single speaker with no background noise
- WAV format preferred, 24kHz+ sample rate
- Professional microphone recommended

### Text Input
- Use natural punctuation for better prosody
- Longer texts generally produce better results
- Avoid special characters or formatting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Credits

- **Chatterbox TTS**: [Resemble AI](https://www.resemble.ai/)
- **Interface**: [Gradio](https://gradio.app/)
- **Integration**: Pinokio Community

## 🐛 Issues

If you encounter any issues, please report them on the [GitHub Issues](https://github.com/PierrunoYT/chatterbox-tts-app/issues) page.
