const fs = require("fs");
module.exports = function (app, db) {
  app.get('/images', (req, res) => {
    // const page = req.query.page
    // const offset = req.query.offset
    // Здесь будем создавать заметку.
    fs.readFile(__dirname + '/docs/images' + ".json", 'utf8', function (err, data) {
      let file = []
      if (data) {
        data = JSON.parse(data)
        // file = data.splice((page - 1) * 10, offset);
      }
      res.send(data);
    });
  });
  app.post('/images', (req, res) => {
    const items = req.body
    // Здесь будем создавать заметку.
    fs.readFile(__dirname + '/docs/images' + ".json", 'utf8', function (err, data) {
      let file = JSON.parse(data ? data : [])
      console.log(typeof file, file)
      file.push({
        user: items.user,
        img: items.img
      })
      console.log(file)
        fs.writeFile(__dirname + '/docs/images' + ".json",  JSON.stringify(file), function (err) {
          if (err) return res.send(err);
          console.log('Hello World > helloworld.txt');
        });
      res.send(200);
    });
  });
};