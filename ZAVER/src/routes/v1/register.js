// routes/v1/register.js

import express from 'express';
const router = express.Router();

// Handle the register route
router.post('/register', (req, res) => {
    res.status(200).json({
        threads: 'this is thread',
        size: 'large',
    });
});

export default router;
