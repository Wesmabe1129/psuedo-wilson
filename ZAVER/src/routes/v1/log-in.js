// routes/v1/log-in.js

import express from 'express';
const router = express.Router();

// Handle the log-in route
router.post('/log-in', (req, res) => {
    const { id } = req.params;
    const { title } = req.body;

    if (!title) {
        return res.status(418).json({ message: 'We need Logo!' });
    }

    res.json({
        title: `your LOGO of ${title} and ID of ${id}`,
        content: 'your content',
        user: 'your user name',
        date: 'date',
    });
});

export default router;
