// // server.js

// const express = require('express');
// const { exec } = require('child_process');

// const app = express();
// const port = 3000;

// // 解析 JSON 请求体
// app.use(express.json());
// // 定义一个简单的 API 端点

// app.post('/api/handleAccounts', (req, res) => {
//     const { homeUrl, platform, opType  } = req.body;
//     exec(`/opt/homebrew/bin/python3.11 example.py ${homeUrl} ${platform} ${opType}`, (error, stdout, stderr) => {
//         if (error) {
//             console.error(`执行 Python 脚本时出错：${error}`);
//             res.status(500).json({ error: 'An error occurred while calling Python script.' });
//             return;
//         }
//         const result = (stdout);
//         res.json({ result });
//     });
// });
// app.use(express.static('public'))
// app.listen(port,'0.0.0.0', () => {
//     console.log(`Server is running at http://localhost:${port}`);
// });
const { exec } = require('child_process');
const express = require('express');
const multer = require('multer');

const xml2js = require('xml2js');
const path = require('path');

const http = require('http');
const WebSocket = require('ws');
const { spawn } = require('child_process');
const session = require('express-session');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;



app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: 'secret_key', // 请替换为一个真正的密钥
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false } // 在生产环境中使用 secure: true
  }));
app.get('/', (req, res) => {
    res.redirect('/login');
  });
  
app.get('/login', (req, res) => {
res.render('login');
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
  
    // 简单的登录验证逻辑
    if ((username === 'administrator' && password === 'password') || (username === 'melody' && password === 'melody')) {
      req.session.loggedIn = true;
      req.session.username = username;
      res.redirect('/dashboard');
    } else {
      res.render('login', { error: 'Invalid username or password' });
    }
  });
app.post('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
        return res.redirect('/dashboard');
        }
        res.redirect('/login');
    });
});
app.get('/dashboard', (req, res) => {
    if (!req.session.loggedIn) {
        return res.redirect('/login');
    }
    res.render('dashboard', { username: req.session.username });
});
app.get('/account', (req, res) => {
    if (!req.session.loggedIn) {
        return res.redirect('/login');
    }
    res.render('account', { username: req.session.username });
    });
app.get('/playwright', (req, res) => {
    if (!req.session.loggedIn) {
        return res.redirect('/login');
    }
    res.render('playwright', { username: req.session.username });
    });
app.get('/playwrightReport', (req, res) => {
    if (!req.session.loggedIn) {
        return res.redirect('/login');
    }
    res.render('playwrightReport', { username: req.session.username });
    });
app.get('/media', (req, res) => {
    if (!req.session.loggedIn) {
        return res.redirect('/login');
    }
    res.render('media', { username: req.session.username });
    });
app.get('/setting', (req, res) => {
    if (!req.session.loggedIn) {
        return res.redirect('/login');
    }
    res.render('setting', { username: req.session.username });
    });
app.use(express.static(path.join(__dirname, 'public')));
app.use('/allure-report', express.static(path.join(__dirname, 'allure-report')));
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', (message) => {
        try {
            const { command, params } = JSON.parse(message);

            if (command === 'run-python') {
                const process = spawn('python3.11', ['backend/account.py', ...params]);

                process.stdout.on('data', (data) => {
                    ws.send(data.toString());
                });

                process.stderr.on('data', (data) => {
                    ws.send(data.toString());
                });

                process.on('close', (code) => {
                    // ws.send(`Process exited with code ${code}`);
                    ws.send('complete');
                });

                process.on('error', (err) => {
                    console.error(`Failed to start subprocess: ${err}`);
                    ws.send(`Error: ${err.message}`);
                });
            }
            if (command === 'run-playwright') {
                const process = spawn('python3.11', ['backend/playwright.py', ...params]);

                process.stdout.on('data', (data) => {
                    ws.send(data.toString());
                });

                process.stderr.on('data', (data) => {
                    ws.send(data.toString());
                });

                process.on('close', (code) => {
                    // ws.send(`Process exited with code ${code}`);
                    ws.send('complete');
                });

                process.on('error', (err) => {
                    console.error(`Failed to start subprocess: ${err}`);
                    ws.send(`Error: ${err.message}`);
                });
            }
        } catch (err) {
            console.error(`Failed to process message: ${err}`);
            ws.send(`Error: ${err.message}`);
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });

    ws.on('error', (err) => {
        console.error(`WebSocket error: ${err}`);
    });
});
//PlaywrightReport.py
app.post('/api/generate-report', (req, res) => {
    exec('python3.11 backend/playwright-allure-report.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            res.status(500).send('Error generating report');
            return;
        }
        res.send('Report generated successfully');
    });
});

//get json
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
const fs = require('fs');

// 读取 JSON 文件并处理数据
// app.get('/test.html', (req, res) => {
//     fs.readFile('record.json', 'utf8', (err, data) => {
//         if (err) {
//             return res.status(500).send('Error reading JSON file');
//         }
//         const jsonData = JSON.parse(data);
//         const valuesList = jsonData.map(item => Object.values(item));
//         res.render('index', { valuesList });
//     });
// });
// function getJsonData(callback) {
//     fs.readFile('record.json', 'utf8', (err, data) => {
//         if (err) {
//             return callback(err, null);
//         }
//         const jsonData = JSON.parse(data);
//         const valuesList = jsonData.map(item => Object.values(item));
//         callback(null, valuesList);
//     });
// }
function getJsonData(callback) {
    fs.readFile('record.json', 'utf8', (err, data) => {
        if (err) {
            return callback(err, null);
        }
        const jsonData = JSON.parse(data);
        callback(null, jsonData);
    });
}
app.get('/history', (req, res) => {
    getJsonData((err, valuesList) => {
        if (!req.session.loggedIn) {
            return res.redirect('/login');
        }
        if (err) {
            return res.status(500).send('Error reading JSON file');
        }
        res.render('history', { title: 'Test Page', valuesList ,username: req.session.username});
    });
});




server.on('error', (err) => {
    console.error(`Server error: ${err}`);
});

const upload = multer({ dest: 'uploads/' });
const xmlFilePath = 'images.xml';

app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

app.post('/upload', upload.single('file'), (req, res) => {
    const filePath = req.file.path;
    const imageUrl = `${req.protocol}://${req.get('host')}/${filePath}`;
    console.log(`File uploaded at: ${filePath}`);
    console.log(`Image URL: ${imageUrl}`);

    fs.readFile(xmlFilePath, 'utf8', (err, data) => {
        if (err && err.code === 'ENOENT') {
            // XML file does not exist, create a new one
            const initialXml = '<?xml version="1.0" encoding="UTF-8"?><images></images>';
            data = initialXml;
        } else if (err) {
            console.error('Error reading XML file:', err);
            return res.status(500).send('Server Error');
        }

        xml2js.parseString(data, (err, result) => {
            if (err) {
                console.error('Error parsing XML:', err);
                return res.status(500).send('Server Error');
            }

            if (!result.images.image) {
                result.images.image = [];
            }

            // Ensure image node is an array
            if (!Array.isArray(result.images.image)) {
                result.images.image = [result.images.image];
            }

            result.images.image.push(imageUrl);

            const builder = new xml2js.Builder();
            const xml = builder.buildObject(result);

            fs.writeFile(xmlFilePath, xml, (err) => {
                if (err) {
                    console.error('Error writing XML file:', err);
                    return res.status(500).send('Server Error');
                }
                console.log('Image URL successfully saved to XML.');
                res.send('Image uploaded and saved to XML');
            });
        });
    });
});

app.get('/images', (req, res) => {
    fs.readFile(xmlFilePath, 'utf8', (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') {
                console.error('XML file does not exist, creating a new one.');
                const initialXml = '<?xml version="1.0" encoding="UTF-8"?><images></images>';
                fs.writeFileSync(xmlFilePath, initialXml, 'utf8');
                return res.json([]);
            } else {
                console.error('Error reading XML file:', err);
                return res.status(500).send('Server Error');
            }
        }

        console.log('XML file content:', data);  // Debug line

        xml2js.parseString(data, (err, result) => {
            if (err) {
                console.error('Error parsing XML:', err);
                return res.status(500).send('Server Error');
            }

            const images = result.images.image || [];
            const imageUrls = images.map(img => typeof img === 'string' ? img : img._);
            console.log('Parsed image URLs:', imageUrls);  // Debug line
            res.json(imageUrls);
        });
    });
});
server.listen(port,'0.0.0.0', () => {
    console.log(`Server running at http://localhost:${port}/`);
});