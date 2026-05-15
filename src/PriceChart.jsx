import React, { useEffect, useRef, memo } from 'react';
import * as LightweightCharts from 'lightweight-charts';

const PriceChart = ({ data, ticker }) => {
  const chartContainerRef = useRef();
  const chartRef = useRef();
  const lineSeriesRef = useRef();
  const volumeSeriesRef = useRef();

  useEffect(() => {
    const container = chartContainerRef.current;
    if (!container) return;

    console.log("Initializing PriceChart for", ticker);
    
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
          borderColor: '#2a2e39',
        },
      });

      const lineSeries = chart.addLineSeries({
        color: '#2962ff',
        lineWidth: 2,
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
      lineSeriesRef.current = lineSeries;
      volumeSeriesRef.current = volumeSeries;
    } catch (e) {
      console.error("Error creating PriceChart:", e);
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
      console.log("Cleaning up PriceChart");
      resizeObserver.disconnect();
      if (chart) chart.remove();
      chartRef.current = null;
    };
  }, [ticker]); // Re-init if ticker changes? No, usually just keep chart. But let's re-init for safety.

  useEffect(() => {
    if (!chartRef.current || !data || data.length === 0) return;

    try {
      const processed = data
        .filter(d => d.time && typeof d.value === 'number')
        .map(d => ({
          time: typeof d.time === 'string' ? d.time : new Date(d.time).toISOString().split('T')[0],
          value: d.value,
          volume: d.volume || 0
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
        lineSeriesRef.current.setData(unique.map(d => ({ time: d.time, value: d.value })));
        volumeSeriesRef.current.setData(unique.map(d => ({ 
          time: d.time, 
          value: d.volume,
          color: '#26a69a44'
        })));
        chartRef.current.timeScale().fitContent();
      }
    } catch (err) {
      console.error("PriceChart Data Update Error:", err);
    }
  }, [data]);

  return <div ref={chartContainerRef} style={{ width: '100%', height: '100%', position: 'relative', minHeight: '200px' }} />;
};

export default memo(PriceChart);
