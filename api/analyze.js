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
        const { text, headlines } = req.body;
        
        if (headlines && Array.isArray(headlines)) {
            const results = [];
            for (const h of headlines) {
                const prediction = await classifier(h);
                const top = prediction[0];
                let score = 0;
                if (top.label === 'positive') score = top.score;
                else if (top.label === 'negative') score = -top.score;
                results.push({ sentiment: top.label, score });
            }
            return res.status(200).json(results);
        }

        if (!text) {
             return res.status(400).json({ success: false, error: "Missing text or headlines" });
        }

        const prediction = await classifier(text);
        let score = 0;
        const top = prediction[0];
        if (top.label === 'positive') score = top.score;
        else if (top.label === 'negative') score = -top.score;

        return res.status(200).json({ sentiment: top.label, score });
    } catch (error) {
        return res.status(500).json({ success: false, error: error.message });
    }
}
