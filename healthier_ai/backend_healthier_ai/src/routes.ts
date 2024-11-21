import { Request, Response } from 'express';
import fs from 'fs';
import axios from 'axios';
import FormData from 'form-data';

export const processImage = async (req: Request, res: Response) => {
    const file = req.file;
    try {
        if (!file) {
            res.status(400).send('No image uploaded');
            return;
        }
        const form = new FormData();
        form.append('file', fs.createReadStream(file.path));

        const response = await axios.post('http://localhost:8080/process-image', form, {
            headers: {
                ...form.getHeaders()
            }
        });

        const result = response.data;
        fs.unlinkSync(file.path);
        res.json(result);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error processing image');
    }
};
