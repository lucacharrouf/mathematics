import express from "express";
import multer from "multer";
import path from "path";
import fs from "fs";
import Video from '../models/videos.model.js';

const router = express.Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        const uploadDir = path.join(process.cwd(), 'backend', 'manim', 'content', 'video_dir');
        
        // Create directory if it doesn't exist
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
        }
        
        cb(null, uploadDir);
    },
    filename: function(req, file, cb) {
        // Use original filename or create a safe one
        const safeName = file.originalname.replace(/[^a-zA-Z0-9_.-]/g, '_');
        cb(null, safeName);
    }
});

// Create the multer upload middleware
const upload = multer({ 
    storage: storage,
    fileFilter: (req, file, cb) => {
        // Accept only video files
        const fileTypes = /mp4|webm|mov|avi|mkv/;
        const extname = fileTypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = fileTypes.test(file.mimetype);
        
        if (extname && mimetype) {
            return cb(null, true);
        } else {
            cb(new Error("Only video files are allowed!"));
        }
    },
    limits: { fileSize: 100 * 1024 * 1024 } // 100MB limit
});

// Get and show all the videos
router.get('/', async (req, res) => {
    try {
        const videos = await Video.find({}).sort({ createdAt: -1 }); // Newest first
        res.status(200).json({ success: true, data: videos });
    } catch (error) {
        console.log("Error in fetching videos: ", error.message);
        res.status(400).json({ success: false, message: "Server error" });
    }
});

// Route to handle video file uploads with form data
router.post('/upload', upload.single('video'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ success: false, message: "No video file provided" });
        }

        const videoData = {
            name: req.body.name || path.basename(req.file.originalname, path.extname(req.file.originalname)),
            topic: req.body.topic || "Unknown Topic",
            videoPath: `/backend/manim/content/videos_dir/${req.file.filename}`, 
            description: req.body.description || "",
            code: req.body.code || "",
            status: "completed"
        };

        const newVideo = new Video(videoData);
        await newVideo.save();

        res.status(201).json({ 
            success: true, 
            message: "Video uploaded successfully", 
            data: newVideo 
        });
    } catch (error) {
        console.log("Error uploading video: ", error.message);
        res.status(500).json({ success: false, message: "Server error" });
    }
});

// Route for Python script to save video metadata and have server copy the video
router.post('/save-from-python', async (req, res) => {
    try {
        const { topic, code, status, videoPath, scenePlan, keyTakeaways } = req.body;
        
        if (!topic) {
            return res.status(400).json({ success: false, message: "Topic is required" });
        }
        
        // Create a safe filename based on the topic
        const safeTopic = topic.replace(/[^a-zA-Z0-9_]/g, '_').toLowerCase();
        
        // If videoPath is provided, check if it exists
        let finalVideoPath = "";
        if (videoPath) {
            // Check if the file exists at the specified path
            if (fs.existsSync(videoPath)) {
                // Copy the file to the videos directory
                const fileName = `${safeTopic}_animation.mp4`;
                const destDir = path.join(process.cwd(), 'backend', 'manim', 'content', 'video_dir');
                
                // Create directory if it doesn't exist
                if (!fs.existsSync(destDir)) {
                    fs.mkdirSync(destDir, { recursive: true });
                }
                
                const destPath = path.join(destDir, fileName);
                
                // Copy the file
                fs.copyFileSync(videoPath, destPath);
                
                // Set the path for database storage (URL format)
                finalVideoPath = `/videos/${fileName}`;
            } else {
                console.log(`Warning: Video file not found at path: ${videoPath}`);
            }
        }
        
        // Create video entry in database
        const videoData = {
            name: `${topic} Animation`,
            topic: topic,
            videoPath: finalVideoPath,
            code: code || "",
            status: status || "completed",
            description: `Animation for ${topic}`,
            scenePlan: scenePlan || "",
            keyTakeaways: keyTakeaways || ""
        };
        
        const newVideo = new Video(videoData);
        await newVideo.save();
        
        res.status(201).json({ 
            success: true, 
            message: "Video data saved successfully", 
            data: newVideo 
        });
    } catch (error) {
        console.log("Error saving video data: ", error);
        res.status(500).json({ success: false, message: "Server error" });
    }
});

// Get a single video by ID
router.get('/:id', async (req, res) => {
    try {
        const video = await Video.findById(req.params.id);
        if (!video) {
            return res.status(404).json({ success: false, message: "Video not found" });
        }
        res.status(200).json({ success: true, data: video });
    } catch (error) {
        console.log("Error fetching video: ", error.message);
        res.status(400).json({ success: false, message: "Server error" });
    }
});

export default router;