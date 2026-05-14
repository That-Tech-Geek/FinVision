import React, { useEffect, useRef, memo } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

const SentimentChart = ({ data, priceData, color }) => {
  const chartContainerRef = useRef();

  useEffect(() => {
    if (!data || data.length === 0) return;

    const handleResize = () => {
      chart.applyOptions({ width: chartContainerRef.current.clientWidth });
    };

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#131722' },
        textColor: '#d1d4dc',
      },
      grid: {
        vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
        horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
      },
      width: chartContainerRef.current.clientWidth,
      height: 500,
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

    // Sentiment Area Series
    const sentimentSeries = chart.addAreaSeries({
      lineColor: color,
      topColor: `${color}44`,
      bottomColor: `${color}00`,
      lineWidth: 2,
      title: 'Sentiment',
    });

    // Price Line Series (Secondary Axis overlay)
    const priceSeries = chart.addLineSeries({
      color: '#2962ff',
      lineWidth: 2,
      lineStyle: 0,
      title: 'Price ($)',
      priceScaleId: 'right', // Overlay on the same scale for visual correlation or use separate?
    });

    // Volume Histogram (Bottom)
    const volumeSeries = chart.addHistogramSeries({
      color: '#26a69a44',
      priceFormat: { type: 'volume' },
      priceScaleId: '', 
    });

    volumeSeries.priceScale().applyOptions({
        scaleMargins: { top: 0.8, bottom: 0 },
    });

    // Data Transformation
    const lineData = data.map(d => ({
      time: d.timestamp,
      value: d.score
    }));

    const volData = data.map(d => ({
      time: d.timestamp,
      value: d.volume || 1,
      color: d.score >= 0 ? '#08998144' : '#f2364544'
    }));

    sentimentSeries.setData(lineData);
    volumeSeries.setData(volData);

    // Integrate Price Data if provided
    if (priceData && priceData.length > 0) {
      // Map priceData timestamps to match sentiment timestamps roughly or just plot directly
      const formattedPrice = priceData.map(p => ({
        time: p.time, // Assuming YFinance uses 'time' as string/timestamp
        value: p.value
      }));
      priceSeries.setData(formattedPrice);
    }

    chart.timeScale().fitContent();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, priceData, color]);

  return <div ref={chartContainerRef} style={{ width: '100%', height: '100%' }} />;
};

export default memo(SentimentChart);
