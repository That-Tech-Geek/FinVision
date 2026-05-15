import { pipeline, env } from '@huggingface/transformers';

// Rule 1: Point cache to the serverless writable /tmp directory
env.cacheDir = '/tmp/hf-transformers-cache';

// Keep the classifier outside the handler to reuse it during warm starts
let classifier = null;

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // Rule 2: Initialize only once per container life cycle
    if (!classifier) {
        try {
            classifier = await pipeline('text-classification', 'Xenova/finbert', {
                quantized: true // Rule 3: Use quantized model for speed and low memory
            });
        } catch (err) {
            return res.status(500).json({ success: false, error: "Model load failed: " + err.message });
        }
    }

    try {
        const { text } = req.body;
        if (!text) {
             return res.status(400).json({ success: false, error: "Missing text" });
        }

        const prediction = await classifier(text);

        // Convert FinBERT labels to scores (-1 to 1)
        // Labels are usually 'positive', 'negative', 'neutral'
        let score = 0;
        const top = prediction[0];
        if (top.label === 'positive') score = top.score;
        else if (top.label === 'negative') score = -top.score;
        else score = 0; // neutral

        return res.status(200).json({ success: true, prediction, score });
    } catch (error) {
        return res.status(500).json({ success: false, error: error.message });
    }
}
