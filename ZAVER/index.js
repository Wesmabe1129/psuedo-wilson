import express from 'express';
import cors from 'cors';
import registerRoutes from './src/routes/v1/register.js';
import loginRoutes from './src/routes/v1/log-in.js';
// import server from './src/routes/v1/server.js';

const app = express();
const PORT = 3000;


app.get('/v1', (req, res) => {
    res.json({
        message: `Server is running`
    })

});

app.use(express.json());
app.use(cors());

// Use the separated routes
app.use('/v1', registerRoutes);
app.use('/v1', loginRoutes);

app.listen(PORT, () => console.log(`Server is running on http://localhost:${PORT}`));
