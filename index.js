const express = require('express')
const app = express()
const port = 5000
const spawn = require("child_process").spawn;

app.get('/createPayload', (req, res) => {
  //spawn('python', ["createPayload.py"]);
  res.send('Created successfully the Wynsure Payload API object')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})