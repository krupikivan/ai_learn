import express from 'express';
import bodyParser from 'body-parser';
import multer from 'multer';
import path from 'path';
import { processImage } from './routes';

const app = express();
const port = 3000;

const storage = multer.diskStorage({
    destination: './uploads/',
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});

// Configure multer for file uploads
const upload = multer({
    storage: storage,
    limits: { fileSize: 30000000 } // 30 MB
}).single('image'); // 'myFile' is the name attribute of the file input field

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/upload', upload, (req, res, next) => {
    console.log('File uploaded:', req.file); // Add this line to debug
    next();
}, processImage);


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
