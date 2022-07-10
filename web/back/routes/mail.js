const fs = require("fs");
module.exports = function (app, db) {
  app.get('/mail', (req, res) => {
    const page = req.query.page
    const offset = req.query.offset
    // Здесь будем создавать заметку.
    fs.readFile(__dirname + '/docs/medium' + ".json", 'utf8', function (err, data) {
      let file = []
      if (data) {
        data = JSON.parse(data)
        file = data.splice((page - 1) * 10, offset);
      }
      res.send(file);
    });
  });
  app.put('/mail', (req, res) => {
    const keys = req.body.keys
    const status = req.body.status
    // Здесь будем создавать заметку.
    fs.readFile(__dirname + '/docs/medium' + ".json", 'utf8', function (err, data) {
      let file = []
      if (data) {
        data = JSON.parse(data)
        for (let i = 0; i < keys.length; i++) {
          data[keys[i]].read = status
        }
        fs.writeFile(__dirname + '/docs/medium' + ".json",  JSON.stringify(data), function (err) {
          if (err) return res.send(err);
          console.log('Hello World > helloworld.txt');
        });
      }
      res.send(200);
    });
  });
};