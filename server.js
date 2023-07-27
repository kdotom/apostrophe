const express = require('express');
const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');

const app = express();

// Add this line to ignore favicon.ico requests
app.get('/favicon.ico', (req, res) => res.status(204));

app.use(express.static('.')); // Serve static files from current directory

app.get('/data', (req, res) => {
    // Load YAML file and send it as JSON
    try {
        const fileContents = fs.readFileSync('flow.yaml', 'utf8');
        const data = yaml.load(fileContents);
        res.json(data);
    } catch (e) {
        console.log(e);
        res.status(500).send('Error loading data');
    }
});

app.get('/', (req, res) => {
    // Send HTML file
    res.sendFile(path.join(__dirname + '/index.html'));
});

const port = 3000;
app.listen(port, () => console.log(`Server is running on http://localhost:${port}`));
