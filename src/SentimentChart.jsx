import React, { useEffect, useRef, memo } from 'react';
import * as LightweightCharts from 'lightweight-charts';

const SentimentChart = ({ data, priceData, color }) => {
  const chartContainerRef = useRef();
  const chartRef = useRef();
  const sentimentSeriesRef = useRef();
  const priceSeriesRef = useRef();
  const volumeSeriesRef = useRef();

  useEffect(() => {
    const container = chartContainerRef.current;
    if (!container) return;

    console.log("Initializing SentimentChart");
    let chart;
    try {
      chart = LightweightCharts.createChart(container, {
        layout: {
          background: { type: LightweightCharts.ColorType.Solid, color: '#131722' },
          textColor: '#d1d4dc',
        },
        grid: {
          vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
          horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
        },
        width: container.clientWidth || 400,
        height: container.clientHeight || 300,
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
          borderColor: '#2a2e39',
        },
        rightPriceScale: {
          borderColor: '#2a2e39',
          autoScale: true,
        }
      });

      const sentimentSeries = chart.addAreaSeries({
        lineColor: color,
        topColor: `${color}44`,
        bottomColor: `${color}00`,
        lineWidth: 2,
        title: 'Sentiment',
      });

      const priceSeries = chart.addLineSeries({
        color: '#2962ff',
        lineWidth: 2,
        lineStyle: 0,
        title: 'Price',
      });

      const volumeSeries = chart.addHistogramSeries({
        color: '#26a69a44',
        priceFormat: { type: 'volume' },
        priceScaleId: '', 
      });

      volumeSeries.priceScale().applyOptions({
          scaleMargins: { top: 0.8, bottom: 0 },
      });

      chartRef.current = chart;
      sentimentSeriesRef.current = sentimentSeries;
      priceSeriesRef.current = priceSeries;
      volumeSeriesRef.current = volumeSeries;
    } catch (e) {
      console.error("Error creating SentimentChart:", e);
      return;
    }

    const handleResize = () => {
      if (container && chart) {
        chart.applyOptions({ 
          width: container.clientWidth,
          height: container.clientHeight
        });
      }
    };

    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(container);

    return () => {
      console.log("Cleaning up SentimentChart");
      resizeObserver.disconnect();
      if (chart) chart.remove();
      chartRef.current = null;
    };
  }, []); // Init once

  useEffect(() => {
    if (!chartRef.current || !data || data.length === 0) return;

    try {
      const processed = data
        .map(d => ({
          time: d.time || d.timestamp,
          value: d.value !== undefined ? d.value : d.score
        }))
        .filter(d => d.time && typeof d.value === 'number')
        .map(d => ({
          time: typeof d.time === 'string' ? d.time : new Date(d.time).toISOString().split('T')[0],
          value: d.value
        }))
        .sort((a, b) => a.time.localeCompare(b.time));

      const unique = [];
      const seen = new Set();
      for (const d of processed) {
        if (!seen.has(d.time)) {
          unique.push(d);
          seen.add(d.time);
        }
      }

      if (unique.length > 0) {
        sentimentSeriesRef.current.setData(unique);
        sentimentSeriesRef.current.applyOptions({ lineColor: color, topColor: `${color}44` });

        const volData = unique.map(d => ({
          time: d.time,
          value: 1,
          color: d.value >= 0 ? '#08998144' : '#f2364544'
        }));
        volumeSeriesRef.current.setData(volData);
      }

      if (priceData && priceData.length > 0) {
        const pProcessed = priceData
          .filter(p => p.time && typeof p.value === 'number')
          .map(p => ({
            time: typeof p.time === 'string' ? p.time : new Date(p.time).toISOString().split('T')[0],
            value: p.value
          }))
          .sort((a, b) => a.time.localeCompare(b.time));

        const pUnique = [];
        const pSeen = new Set();
        for (const p of pProcessed) {
          if (!pSeen.has(p.time)) {
            pUnique.push(p);
            pSeen.add(p.time);
          }
        }
        priceSeriesRef.current.setData(pUnique);
      }

      chartRef.current.timeScale().fitContent();
    } catch (err) {
      console.error("SentimentChart Data Update Error:", err);
    }
  }, [data, priceData, color]);

  return <div ref={chartContainerRef} style={{ width: '100%', height: '100%', position: 'relative', minHeight: '200px' }} />;
};

export default memo(SentimentChart);
