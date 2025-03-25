import mongoose from 'mongoose'

const videoSchema = new mongoose.Schema(
  {
    topic: {
      type: String,
      required: true,
    },
    code: {
      type: String,
      required: true,
    },
    status: {
      type: String,
      required: true,
      enum: ['pending', 'completed', 'failed'],
      default: 'pending',
    },
    videoPath: {
      type: String,
      default: '',
    },
    scenePlan: {
      type: String,
      default: '',
    },
    keyTakeaways: {
      type: String,
      default: '',
    },
  },
  {
    timestamps: true,
  }
)

const Video = mongoose.model('Video', videoSchema)

export default Video 