import { pipeline } from '@huggingface/transformers';
import express from 'express';
import bodyParser from 'body-parser';

const app = express();
app.use(bodyParser.json());

let classifier;

// Initialize model
async function init() {
    console.log('Loading FinBERT model into memory...');
    classifier = await pipeline('text-classification', 'Xenova/finbert', { 
        quantized: true 
    });
    console.log('FinBERT model loaded.');
}

app.post('/analyze', async (req, res) => {
    try {
        const { headlines } = req.body;
        console.log(`Received ${headlines?.length} headlines for analysis`);
        if (!headlines || !Array.isArray(headlines)) {
            return res.status(400).json({ error: 'headlines must be an array' });
        }

        const results = [];
        for (const title of headlines) {
            const output = await classifier(title);
            results.push({
                title,
                sentiment: output[0].label,
                score: output[0].score
            });
        }
        res.json(results);
    } catch (error) {
        console.error('Analysis error:', error);
        res.status(500).json({ error: error.message });
    }
});

const PORT = 3001;
init().then(() => {
    app.listen(PORT, () => {
        console.log(`Sentiment Analysis Sidecar listening on port ${PORT}`);
    });
});
