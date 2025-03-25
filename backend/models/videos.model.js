import mongoose from "mongoose";

const videoSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    videoPath: {
        type: String, 
        required: true
    },   
    status: {
        type: String,
        enum: ['pending', 'processing', 'completed', 'failed'],
        default: 'pending'
    } 
}, {
    timestamps: true
});

const Video = mongoose.model('Video', videoSchema);

export default Video;