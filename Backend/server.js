require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
    
  })
  .then(() => console.log("MongoDB Connected"))
  .catch((err) => console.error("MongoDB connection error:", err));
  

// Define News Schema & Model
const newsSchema = new mongoose.Schema({
  headline: String,
  author: String,
  published_date: String,
  summary: String,
  content: String,
  image_url: String,
  source_link: String,
});

const News = mongoose.model("articles", newsSchema);

// API Route to Fetch All News
app.get("/news", async (req, res) => {
    try {
      const newsData = await News.find();  // Fetch all documents from MongoDB
      
      res.json(newsData);
    } catch (error) {
      res.status(500).json({ message: "Error fetching news", error });
    }
  });
  
// Start Server
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
