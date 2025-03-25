import mongoose from 'mongoose'

export const connectDB = async () => {
  try {
    const connectionString = process.env.MONGODB_KEY
    
    // Debug to make sure the connection string is available
    console.log("Connection string:", connectionString)
    
    if (!connectionString) {
      throw new Error('MongoDB connection string is undefined. Check your .env.db file.')
    }
    
    const conn = await mongoose.connect(connectionString)
    
    console.log(`MongoDB Connected: ${conn.connection.host}`)
  } catch (error) {
    console.error(`Error: ${error.message}`)
    process.exit(1)
  }
}