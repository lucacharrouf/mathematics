import express from 'express'
import dotenv from 'dotenv'
import cors from 'cors' // Add CORS support
import path from 'path' // For file paths
import { fileURLToPath } from 'url' // For ES modules __dirname
import { connectDB } from './config/db.js'
import videoRoutes from './routes/video.route.js'
import inputRoutes from './routes/input.route.js'
import feedbackRoutes from './routes/feedback.route.js'
import fs from 'fs' // For file system operations
import { spawn } from 'child_process'

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Load environment variables from .env file
dotenv.config({ path: path.join(process.cwd(), '.env') })

// Initialize Express app
const app = express()

// CORS configuration
const corsOptions = {
  origin: 'http://localhost:5175',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Accept'],
  credentials: false,
  optionsSuccessStatus: 200
};

// Apply cors middleware with options
app.use(cors(corsOptions));

// Basic middleware
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Move these definitions to the top of the file, after the imports but before middleware
const videoDir = path.join(process.cwd(), 'backend', 'manim', 'content', 'video_dir');
const videosDir = path.join(process.cwd(), 'backend', 'manim', 'content', 'videos_dir');

// 1. First, all middleware and debugging
app.use((req, res, next) => {
  console.log('\n=== CORS Debug ===');
  console.log('Origin:', req.headers.origin);
  console.log('Method:', req.method);
  console.log('Headers:', req.headers);
  next();
});

// 2. Add general request logging middleware
app.use((req, res, next) => {
  console.log(`\n=== Incoming Request ===`);
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  console.log('Headers:', req.headers);
  if (req.method !== 'GET') {
    console.log('Body:', req.body);
  }
  next();
});

// 3. Static file serving
app.use('/videos-content', express.static(videoDir));
app.use('/videos-content', express.static(videosDir));

// 4. Basic routes first
app.get('/', (req, res) => {
  console.log('Root route hit');
  res.json({ status: 'ok', message: 'Server is running' });
});

app.get('/test', (req, res) => {
  console.log('Test endpoint hit');
  res.json({ status: 'ok', message: 'Server is working' });
});

app.get('/cors-debug', (req, res) => {
  console.log('=== CORS Debug Info ===');
  console.log('Request Origin:', req.headers.origin);
  console.log('Request Method:', req.method);
  console.log('Request Headers:', req.headers);
  
  res.json({
    message: 'CORS Debug Info',
    origin: req.headers.origin,
    method: req.method,
    headers: req.headers
  });
});

app.get('/ping', (req, res) => {
  res.json({ pong: true, time: new Date().toISOString() });
});

app.get('/check-videos', (req, res) => {
  try {
    // Check both possible directories
    const results = {
      singular: { exists: false, files: [] },
      plural: { exists: false, files: [] }
    };
    
    // Check singular directory (video_dir)
    if (fs.existsSync(videoDir)) {
      results.singular.exists = true;
      results.singular.path = videoDir;
      results.singular.files = fs.readdirSync(videoDir);
    }
    
    // Check plural directory (videos_dir)
    if (fs.existsSync(videosDir)) {
      results.plural.exists = true;
      results.plural.path = videosDir;
      results.plural.files = fs.readdirSync(videosDir);
    }
    
    res.json({ 
      success: true,
      results: results
    });
  } catch (err) {
    res.json({ 
      success: false, 
      error: err.message 
    });
  }
});

app.get('/cors-test', (req, res) => {
  console.log('CORS test endpoint hit');
  console.log('Origin:', req.headers.origin);
  res.json({ 
    status: 'ok', 
    message: 'CORS is working',
    origin: req.headers.origin,
    headers: req.headers
  });
});

app.post('/test-endpoint', (req, res) => {
  console.log('Test endpoint hit with body:', req.body);
  res.json({
    success: true,
    message: 'Test endpoint working',
    receivedData: req.body
  });
});

app.post('/generate-video', async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  
  console.log('\n=== Processing Video Generation Request ===');
  console.log('Request Body:', req.body);
  
  const { topic, macroTopic, problemType } = req.body;

  // Validate input
  if (!topic || !macroTopic || !problemType) {
    console.log('Validation failed:', { topic, macroTopic, problemType });
    return res.status(400).json({ 
      success: false, 
      error: 'Missing required fields',
      received: { topic, macroTopic, problemType }
    });
  }

  try {
    // Log the current working directory
    console.log('Current working directory:', process.cwd());
    
    // Construct path to main_exercise.py
    const scriptPath = path.join(process.cwd(), 'backend', 'manim', 'main_exercise.py');
    console.log('Looking for Python script at:', scriptPath);
    
    // Check if script exists
    if (!fs.existsSync(scriptPath)) {
      console.error('Python script not found!');
      return res.status(500).json({
        success: false,
        error: 'Python script not found',
        path: scriptPath
      });
    }
    
    console.log('Python script found, preparing to execute');

    // Prepare command arguments
    const commandArgs = [
      scriptPath,
      '--topic', topic,
      '--macro-topic', macroTopic,
      '--problem-type', problemType,
      '--server-url', 'http://localhost:4000'
    ];

    console.log('Executing command:', 'python', commandArgs.join(' '));

    // Spawn Python process
    const pythonProcess = spawn('python', commandArgs);

    let outputData = '';
    let errorData = '';

    pythonProcess.stdout.on('data', (data) => {
      const output = data.toString();
      outputData += output;
      console.log('Python output:', output);
    });

    pythonProcess.stderr.on('data', (data) => {
      const error = data.toString();
      errorData += error;
      console.error('Python error:', error);
    });

    pythonProcess.on('close', (code) => {
      console.log(`\n=== Python Process Completed ===`);
      console.log('Exit code:', code);
      console.log('Total output length:', outputData.length);
      console.log('Total error length:', errorData.length);
      
      if (code !== 0) {
        console.error('Process failed with code:', code);
        console.error('Error output:', errorData);
        return res.status(500).json({ 
          success: false, 
          error: 'Python process failed',
          details: errorData,
          exitCode: code
        });
      }

      try {
        // Try to find the video path in the output
        const videoPathMatch = outputData.match(/Video saved to: (.+)/);
        
        if (!videoPathMatch) {
          console.error('No video path found in output');
          return res.status(500).json({ 
            success: false, 
            error: 'Video path not found in output',
            output: outputData
          });
        }

        const videoPath = videoPathMatch[1];
        console.log('Found video path:', videoPath);

        const videoFileName = path.basename(videoPath);
        const videoUrl = `/videos-content/${videoFileName}`;
        
        console.log('Generated video URL:', videoUrl);
        console.log('Sending success response');

        return res.json({ 
          success: true, 
          videoUrl,
          message: 'Video generated successfully'
        });
      } catch (error) {
        console.error('Error processing Python output:', error);
        return res.status(500).json({
          success: false,
          error: 'Error processing Python output',
          details: error.message
        });
      }
    });

  } catch (error) {
    console.error('Server error:', error);
    return res.status(500).json({ 
      success: false, 
      error: 'Internal server error',
      details: error.message
    });
  }
});

// 6. Other API routes
app.use("/videos", videoRoutes);
app.use("/input", inputRoutes);
app.use("/feedback", feedbackRoutes);

// 7. 404 handler should be last (before error handler)
app.use((req, res) => {
  console.log(`Route not found: ${req.method} ${req.path}`);
  res.status(404).json({
    success: false,
    error: 'Route not found',
    path: req.path,
    method: req.method
  });
});

// 8. Error handling middleware is the very last
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({ 
    success: false, 
    error: err.message || 'Internal server error'
  });
});

// Check if video directories exist and log their contents
try {
  if (fs.existsSync(videoDir)) {
    console.log('Singular video_dir exists');
    const files = fs.readdirSync(videoDir);
    console.log('Files in video_dir:', files);
  } else {
    console.log('Singular video_dir does not exist');
  }
  
  if (fs.existsSync(videosDir)) {
    console.log('Plural videos_dir exists');
    const files = fs.readdirSync(videosDir);
    console.log('Files in videos_dir:', files);
  } else {
    console.log('Plural videos_dir does not exist');
  }
} catch (err) {
  console.error('Error checking video directories:', err);
}

// Start server
const PORT = process.env.PORT || 4000
app.listen(PORT, () => {
    connectDB()
    console.log(`Server is ready at http://localhost:${PORT}`)
    console.log(`Video files will be served from both directories:`)
    console.log(`- ${videoDir}`)
    console.log(`- ${videosDir}`)
})

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
});