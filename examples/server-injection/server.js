const http = require('http');
const url = require('url');

const port = 3000;

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    const trimmedPath = path.replace(/^\/+|\/+$/g, '');

    if (trimmedPath === 'submit' && req.method === 'POST') {
        handlePostRequest(req, res);
    } else {
        notFoundHandler(res);
    }
});

function handlePostRequest(req, res) {
    let body = '';

    req.on('data', (chunk) => {
        body += chunk.toString();
    });

    req.on('end', () => {
        console.log('Received data:', body);

        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end('Received data: ' + body);
    });
}

function notFoundHandler(res) {
    res.writeHead(404, {'Content-Type': 'text/plain'});
    res.end('404 Not Found');
}

server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
