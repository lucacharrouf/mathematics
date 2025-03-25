router.post('/generate-video', async (req, res) => {
  const { topic, audience } = req.body;
  
  try {
    // Spawn a child process to run the Python script
    const pythonProcess = spawn('python', [
      'backend/manim/main.py',
      '--topic', topic,
      '--audience', audience
    ]);

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        res.json({ success: true });
      } else {
        res.status(500).json({ success: false, error: 'Video generation failed' });
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Failed to start video generation' });
  }
}); 