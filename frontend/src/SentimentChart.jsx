import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

const SentimentChart = ({ data, color }) => {
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
      }
    });

    const series = chart.addAreaSeries({
      lineColor: color,
      topColor: `${color}44`,
      bottomColor: `${color}00`,
      lineWidth: 2,
    });

    const volumeSeries = chart.addHistogramSeries({
      color: '#26a69a44',
      priceFormat: {
          type: 'volume',
      },
      priceScaleId: '', // set as overlay
    });

    volumeSeries.priceScale().applyOptions({
        scaleMargins: {
            top: 0.8,
            bottom: 0,
        },
    });

    // Format data for lightweight-charts
    // data is [{timestamp: 123, score: 0.5, volume: 10}, ...]
    const lineData = data.map(d => ({
      time: d.timestamp,
      value: d.score
    }));

    const volData = data.map(d => ({
      time: d.timestamp,
      value: d.volume || 1, // Minimum 1 if entry exists
      color: d.score >= 0 ? '#08998144' : '#f2364544'
    }));

    series.setData(lineData);
    volumeSeries.setData(volData);

    chart.timeScale().fitContent();

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, color]);

  return <div ref={chartContainerRef} style={{ width: '100%', height: '100%' }} />;
};

export default SentimentChart;
