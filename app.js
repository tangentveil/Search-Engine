const express = require('express');
const ejs = require('ejs');
const port = process.env.port || 3000;
const app = express();
const path = require('path');
const controller = require('./controllers/controller');

// view engine
app.set('view engine', 'ejs');

// static
app.use(express.static('./public'));

// fire contoller
controller(app);

// port listening
app.listen(port, ()=>{
    console.log(`Listening on port : ${port}`);
});