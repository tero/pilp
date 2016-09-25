import express from 'express'
import {SimpleDB} from 'aws-sdk'

var app = express()
var db = new SimpleDB({region: 'eu-west-1'})

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/', (req, res) => {
  res.send('Hello World')
})

app.get('/api/pilp-temperatures', (req, res) => {
  var date = new Date(Date.now() - (24 * 3600 * 1000))
  db.select(
    {
      SelectExpression: `select * from \`pilp.logs\` where itemName() > '${date.toISOString()}' order by itemName() asc`
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err)
      }

      res.send(data.Items)
    }
  )
})

app.get('/api/pilp-temperatures/latest', (req, res) => {
  db.select(
    {
      SelectExpression: "select * from `pilp.logs` where itemName() like '2016%' order by itemName() desc limit 1"
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err)
      }

      res.send(data.Items)
    }
  )
})

app.listen(3000)
