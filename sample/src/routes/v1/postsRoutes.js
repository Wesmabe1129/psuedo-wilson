// postsRoutes.js
import express from 'express';
import { getPosts, getPostById, getPostComments, getCommentReplies } from '../../controllers/v1/postsController.js';

const postsRouter = express.Router();

// Route to get posts with optional query parameters: limits, offset, sortBy
postsRouter.get('/', getPosts);

// Route to get a specific post by ID
postsRouter.get('/:postId', getPostById);

// Route to get comments for a specific post
postsRouter.get('/:postId/comments', getPostComments);

// Route to get replies for a specific comment on a post
postsRouter.get('/:postId/comments/:commentId/replies', getCommentReplies);

export default postsRouter;
