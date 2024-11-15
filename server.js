const express = require('express');
const cors = require('cors');
const path = require('path');
const rateLimit = require('express-rate-limit'); // Import express-rate-limit

const app = express();
const port = 5001;

// Apply rate limiting to all requests
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Allow only 100 requests per 15 minutes per IP
    message: 'Too many requests, please try again later.'
});

app.use(limiter); // Use the rate limiter

app.use(cors());
app.use(express.json());

// Serve static files (images) from the 'images' folder
app.use('/images', express.static(path.join(__dirname, 'images')));

// Sample images data
const images = [
    { id: 1, title: 'Middle East', url: 'middle_east.png' }
];

app.get('/search', (req, res) => {
    const query = req.query.q;

    if (!query) {
        return res.status(400).json({ error: 'Query parameter is required' });
    }

    const filteredImages = images.filter(item => item.title.toLowerCase().includes(query.toLowerCase()));

    if (filteredImages.length === 0) {
        return res.status(404).json({ error: 'No images found' });
    }

    return res.json(filteredImages);
});

app.listen(port, '127.0.0.1', () => {
    console.log(`Server running on http://127.0.0.1:${port}`);
});
