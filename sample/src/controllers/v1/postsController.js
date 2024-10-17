// postsController.js
import { connection } from '../../core/database.js'; // Make sure this file is also using ES module syntax

/**
 * Get posts with optional filters: limits, offset, and sortBy
 */
export const getPosts = async (req, res) => {
  try {
    const { limits = 10, offset = 0, sortBy = 'relevancy' } = req.query;

    const posts = await connection.query(`
      SELECT * FROM posts 
      ORDER BY ${sortBy} 
      LIMIT ? OFFSET ?
    `, [parseInt(limits), parseInt(offset)]);

    res.json({ success: true, data: posts });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Failed to fetch posts' });
  }
};

/**
 * Get a specific post by ID
 */
export const getPostById = async (req, res) => {
  try {
    const { postId } = req.params;

    const post = await db.query(`SELECT * FROM posts WHERE id = ?`, [postId]);

    if (post.length === 0) {
      return res.status(404).json({ success: false, message: 'Post not found' });
    }

    res.json({ success: true, data: post[0] });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Failed to fetch post' });
  }
};

/**
 * Get comments for a specific post
 */
export const getPostComments = async (req, res) => {
  try {
    const { postId } = req.params;

    const comments = await db.query(`SELECT * FROM comments WHERE post_id = ?`, [postId]);

    res.json({ success: true, data: comments });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Failed to fetch comments' });
  }
};

/**
 * Get replies for a specific comment on a post
 */
export const getCommentReplies = async (req, res) => {
  try {
    const { postId, commentId } = req.params;

    const replies = await db.query(`SELECT * FROM replies WHERE post_id = ? AND comment_id = ?`, [postId, commentId]);

    res.json({ success: true, data: replies });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Failed to fetch replies' });
  }
};
