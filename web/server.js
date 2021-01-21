const express = require('express');
const path = require('path');
const port = 9005;
const app = express();
const fs = require('fs');
const dirname = __dirname
const build = dirname + '/build/';
app.use(express.static(build));

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
            fromDir(filename, filter); //recurse
        }
        else if (filename.indexOf(filter) >= 0) {
            console.log('-- found: ', filename);
        };
    };
};
fromDir('./', '.html');

app.get('*', function (req, res) {
    const index = path.join(dirname, 'build', 'index.html');
    res.sendFile(index);
});

app.listen(port);
