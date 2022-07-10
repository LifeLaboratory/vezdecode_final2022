const express = require('express')
const app = express()
const port = 3001
const cors = require('cors')
const useragent = require("express-useragent")
app.use(express.json());
app.use(useragent.express());
app.use(cors())
require('./routes')(app, {});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
