import asyncio
import json
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime
from ingestion import KeyRotator, SentimentProcessor, FirestoreBatchedWriter, IngestionEngine

class TestIngestionEngine(unittest.TestCase):

    def test_key_rotation(self):
        keys = ["key1", "key2", "key3"]
        rotator = KeyRotator(keys)
        self.assertEqual(rotator.get_key(), "key1")
        self.assertEqual(rotator.get_key(), "key2")
        self.assertEqual(rotator.get_key(), "key3")
        self.assertEqual(rotator.get_key(), "key1")

    def test_sentiment_ensemble(self):
        processor = SentimentProcessor()
        # Positive text
        pos_score = processor.analyze("This is amazing news! I love this stock.")
        self.assertGreater(pos_score, 0)
        
        # Negative text
        neg_score = processor.analyze("Terrible performance, avoid at all costs.")
        self.assertLess(neg_score, 0)
        
        # Neutral
        neutral_score = processor.analyze("The stock price remained unchanged today.")
        self.assertAlmostEqual(neutral_score, 0, delta=0.2)

    def test_batched_writer(self):
        mock_db = MagicMock()
        mock_batch = MagicMock()
        mock_batch.commit = AsyncMock()
        mock_db.batch.return_value = mock_batch
        
        writer = FirestoreBatchedWriter(mock_db, batch_size=3)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_test():
            await writer.add("coll", "id1", {"val": 1})
            await writer.add("coll", "id2", {"val": 2})
            # Batch not yet full
            mock_batch.commit.assert_not_called()
            
            await writer.add("coll", "id3", {"val": 3})
            # Batch should flush now
            mock_batch.commit.assert_called_once()
            self.assertEqual(len(writer.queue), 0)
            
        loop.run_until_complete(run_test())

    @patch("websockets.connect")
    def test_websocket_reconnection(self, mock_connect):
        # mock_ws must be a mock that supports async iterator and async context manager
        mock_ws = MagicMock()
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)
        mock_ws.send = AsyncMock()
        mock_ws.__aiter__ = MagicMock(return_value=AsyncMock())
        mock_ws.__aiter__.return_value.__anext__ = AsyncMock(side_effect=[
            json.dumps({"type": "trade", "data": []}),
            StopAsyncIteration
        ])
        
        mock_connect.side_effect = [Exception("Conn fail"), mock_ws]
        
        engine = IngestionEngine(MagicMock(), ["AAPL"], ["key1"])
        engine.manager.active = True
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_test():
            # We only run for a short bit
            task = asyncio.create_task(engine.manager.connect_and_listen())
            await asyncio.sleep(1.5) # Allow one retry (initial delay is 1s)
            engine.stop()
            try:
                await asyncio.wait_for(task, timeout=1)
            except asyncio.TimeoutError:
                pass
            
            self.assertGreaterEqual(mock_connect.call_count, 2)
            
        loop.run_until_complete(run_test())

if __name__ == "__main__":
    unittest.main()
