const { spawn } = require('child_process');
const path = require('path');

router.post('/generate-video', async (req, res) => {
  const { topic, audience } = req.body;
  
  try {
    // Construct the proper path to main.py
    const pythonScript = path.join(__dirname, '..', 'manim', 'main.py');
    
    // Spawn python process with proper arguments
    const pythonProcess = spawn('python3', [
      pythonScript,
      '--topic', topic,
      '--audience', audience
    ]);

    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
      console.log('Python output:', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
      console.error('Python error:', data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        res.json({ 
          success: true,
          message: 'Video generated successfully',
          output: output
        });
      } else {
        res.status(500).json({ 
          success: false, 
          error: 'Video generation failed',
          output: output,
          errorOutput: errorOutput
        });
      }
    });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: 'Failed to start video generation',
      details: error.message
    });
  }
}); 