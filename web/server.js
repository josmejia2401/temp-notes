const express = require('express');
const path = require('path');
const port = 9005;
const app = express();
const fs = require('fs');
app.use(express.static(path.join(__dirname, 'build')));

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Authorization, X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Allow-Request-Method');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
    res.header('Allow', 'GET, POST, OPTIONS, PUT, DELETE');
    next();
});

app.get('/service-worker.js', function (req, res) {
    const index = path.join(__dirname, 'src', 'serviceWorker.js');
    res.sendFile(index);
});

app.get('/notes/**', function (req, res) {
    var arrayx = req.url.split("/");
    arrayx = arrayx.slice(1);
    arrayx = arrayx.slice(1);
    const index = path.join(__dirname, 'build', arrayx.join('/'));
    if (fs.existsSync(index)) {
        res.sendFile(index);
    } else {
        const index = path.join(__dirname, 'build', 'index.html');
        res.sendFile(index);    
    }
});

app.get('/', function (req, res) {
    const index = path.join(__dirname, 'build', 'index.html');
    res.sendFile(index);
});

app.get('*', function (req, res) {
    const index = path.join(__dirname, 'build', 'index.html');
    res.sendFile(index);
});

app.listen(port);


/*
app.all('*', function(req, res, next){
    console.log('app.all');
    if (!req.get('Origin')) return next();
    res.set('Access-Control-Allow-Origin', '*');
    res.set('Access-Control-Allow-Methods', 'GET');
    res.set('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type');
    if ('OPTIONS' == req.method) return res.send(200);
    next();
});
function fromDir(startPath, filter) {
    if (!fs.existsSync(startPath)) {
        console.log("no dir ", startPath);
        return;
    }
    var files = fs.readdirSync(startPath);
    for (var i = 0; i < files.length; i++) {
        var filename = path.join(startPath, files[i]);
        var stat = fs.lstatSync(filename);
        if (stat.isDirectory()) {
            fromDir(filename, filter);
        }
        else if (filename.indexOf(filter) >= 0) {
            console.log('-- found: ', filename);
        };
    };
};
fromDir('./', '.html');*/