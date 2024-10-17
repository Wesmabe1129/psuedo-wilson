// index.js in routes/v1
import { Router } from 'express';
import homeRouter from './homeRoutes.js';
import accountRouter from './accountRoutes.js';
import postsRouter from './postsRoutes.js';

const v1 = new Router();

v1.use('/account', accountRouter);
v1.use('/posts', postsRouter); // Correctly register postsRouter here
v1.use('/', homeRouter); // Ensure this is at the end

export default v1;
