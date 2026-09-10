module.exports = {
  run: [{
    method: "shell.run",
    params: {
      message: "git pull --ff-only"
    }
  }, {
    method: "script.start",
    params: {
      uri: "install.js"
    }
  }]
}
