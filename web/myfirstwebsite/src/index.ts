import express from 'express';
import path from 'path';
import crypto from 'crypto';
import cookieParser from 'cookie-parser';
import fs from 'fs';

import jwt from 'jsonwebtoken';

const key = crypto.randomBytes(32);
const app = express();
const flag = fs.readFileSync('flag.txt', 'utf-8').trim();

app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

function verifyToken(token: string | undefined) {
    try {
        return token ? jwt.verify(token, key, { algorithms: ['HS256'] }) : undefined;
    }
    catch (e) {
        console.warn(e);
        return undefined;
    }
}

app.get("/", (req, res) => {
    if (req.cookies['token'] && !verifyToken(req.cookies['token']))
        res.clearCookie('token');
    // res.cookie('token', jwt.sign({ testkey: 'testvalue' }, key, { algorithm: 'HS256' }));
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get("/login", (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});
app.post("/login", (req, res) => {
    const payload = req.body;
    // console.log(payload);
    res.cookie('token', jwt.sign(payload, key, { algorithm: 'HS256' }));
    res.redirect('/');
});

app.get("/robots.txt", (req, res) => {
    res.type('text/plain');
    res.sendFile(path.join(__dirname, 'robots.txt'));
});


// ADMIN
app.get("/admin", (req, res) => {
    try {
        const payload: any = verifyToken(req.cookies['token']);
        console.log(payload);
        if (payload && payload['username'] === 'admin' && payload['isAdmin'] === 'true') {
            res.send(`Welcome admin! Here is your flag: ${flag}`);
            return;
        }
    }
    catch (e) {
        console.warn(e);
    }
    res.clearCookie('token');
    res.sendFile(path.join(__dirname, "admin.html"));
});

app.get("/admin/login", (req, res) => {
    res.sendFile(path.join(__dirname, 'admin_login.html'));
});
app.post("/admin/login", (req, res) => {
    res.redirect('/admin');
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
    console.log('Key is', key.toString('hex'));
});
