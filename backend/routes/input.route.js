// routes/input.route.js
import express from 'express'
import Input from '../models/input.model.js' // You'll need to create this model

const router = express.Router()

// Add this route to handle the data from Python
router.post('/save-from-python', async (req, res) => {
  try {
    console.log('Received data from Python:', req.body)
    
    // Create a new document using your model
    const newInput = new Input({
      topic: req.body.topic,
      code: req.body.code,
      status: req.body.status
    })
    
    // Save to MongoDB
    const savedInput = await newInput.save()
    
    res.status(201).json({
      success: true,
      message: 'Data saved successfully',
      data: savedInput
    })
  } catch (error) {
    console.error('Error saving input data:', error)
    res.status(400).json({
      success: false,
      message: 'Failed to save data',
      error: error.message
    })
  }
})

router.post('/update-feedback', async (req, res) => {
    try {
      const { topic, feedback, rating } = req.body;
      
      if (!topic || !feedback) {
        return res.status(400).json({ error: 'Topic and feedback are required' });
      }
      
      console.log(`Updating feedback for topic: ${topic}`);
      console.log(`Feedback content: ${feedback.substring(0, 50)}...`);
      if (rating) console.log(`Rating: ${rating}`);
      
      // Find the input document by topic
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
      console.log(`Successfully updated feedback for topic: ${topic}`);
      
      return res.status(200).json({ 
        message: 'Feedback saved successfully',
        id: inputDoc._id
      });
    } catch (error) {
      console.error('Error saving feedback:', error);
      return res.status(500).json({ error: 'Server error saving feedback' });
    }
  });

// Route to get all topics
router.get('/topics', async (req, res) => {
    try {
      // Find all input documents and only select the topic field
      const inputs = await Input.find({}, 'topic');
      
      // Extract the topic names into an array
      const topics = inputs.map(input => input.topic);
      
      // Return the list of topics
      return res.status(200).json(topics);
    } catch (error) {
      console.error('Error fetching topics:', error);
      return res.status(500).json({ error: 'Server error fetching topics' });
    }
  });

export default router