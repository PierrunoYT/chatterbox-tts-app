module.exports = {
  run: [{
    when: "{{exists('installed.flag')}}",
    method: "fs.rm",
    params: {
      path: "installed.flag"
    }
  }, {
    when: "{{exists('app/env')}}",
    method: "fs.rm",
    params: {
      path: "app/env"
    }
  }]
}
