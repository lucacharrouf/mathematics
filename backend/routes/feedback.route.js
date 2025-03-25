import express from 'express';
import Input from '../models/input.model.js';
const router = express.Router();

// Route to save feedback
router.post('/save', async (req, res) => {
  try {
    const { topic, feedback, rating } = req.body;
    
    if (!topic || !feedback) {
      return res.status(400).json({ error: 'Topic and feedback are required' });
    }
    
    // Find the existing input document by topic
    const inputDoc = await Input.findOne({ topic });
    
    if (!inputDoc) {
      return res.status(404).json({ 
        error: 'No input found with this topic',
        topic: topic
      });
    }
    
    // Update the input document with feedback
    inputDoc.feedback = feedback;
    
    // Update rating if provided
    if (rating && rating >= 1 && rating <= 5) {
      inputDoc.rating = rating;
    }
    
    // Save the updated document
    await inputDoc.save();
    
    return res.status(200).json({ 
      message: 'Feedback saved successfully',
      id: inputDoc._id
    });
  } catch (error) {
    console.error('Error saving feedback:', error);
    return res.status(500).json({ error: 'Server error saving feedback' });
  }
});

// Route to get feedback for a topic
router.get('/:topic', async (req, res) => {
  try {
    const { topic } = req.params;
    
    // Find the input document by topic
    const inputDoc = await Input.findOne({ topic });
    
    if (!inputDoc) {
      return res.status(404).json({ error: 'No input found with this topic' });
    }
    
    // Return the feedback and rating
    return res.status(200).json({
      topic: inputDoc.topic,
      feedback: inputDoc.feedback || '',
      rating: inputDoc.rating || null,
      timestamp: inputDoc.updatedAt
    });
  } catch (error) {
    console.error('Error fetching feedback:', error);
    return res.status(500).json({ error: 'Server error fetching feedback' });
  }
});

export default router;