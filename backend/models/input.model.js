// Check if your input.model.js has these fields
import mongoose from "mongoose";

const inputSchema = new mongoose.Schema({
    topic: {
        type: String,
        required: true
    },
    code: {
        type: String,
        required: true
    },
    status: {
        type: String,
        enum: ['pending', 'completed', 'failed'],
        default: 'pending'
    },
    timestamp: {
        type: Date,
        default: Date.now
    },
    rating: {
        type: Number,
        min: 1,
        max: 5,
    },
    feedback: {
        type: String,
    }
}, {
    timestamps: true
});

const Input = mongoose.model('Input', inputSchema);

export default Input;