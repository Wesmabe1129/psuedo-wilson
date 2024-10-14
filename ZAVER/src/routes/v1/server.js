// routes/v1/server.js

import express from 'express';
const router = express.Router();

// Handle the register route
router.get('/register', (req, res) => {
    res.status(200).json({
        message: "Server is running on http://localhost:3000"
    });
});

export default router;