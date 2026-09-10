// Keep these versions aligned with Chatterbox's torch/torchaudio requirements.
const packages = "torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0"
const install = (when, index) => ({
  ...(when ? { when } : {}),
  method: "shell.run",
  params: {
    venv: "{{args && args.venv ? args.venv : 'env'}}",
    path: "{{args && args.path ? args.path : 'app'}}",
    message: `uv pip install ${packages} --index-url ${index} --reinstall-package torch --reinstall-package torchvision --reinstall-package torchaudio`
  },
  next: null
})

module.exports = {
  run: [
    install("{{gpu === 'nvidia' && (platform === 'win32' || platform === 'linux')}}", "https://download.pytorch.org/whl/cu124"),
    install("{{gpu === 'amd' && platform === 'linux'}}", "https://download.pytorch.org/whl/rocm6.2.4"),
    install("{{platform === 'darwin' && arch === 'arm64'}}", "https://pypi.org/simple"),
    // AMD on Windows uses CPU: DirectML requires an incompatible torch version.
    install(null, "https://download.pytorch.org/whl/cpu")
  ]
}
