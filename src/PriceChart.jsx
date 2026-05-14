import React, { useEffect, useRef, memo } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

const PriceChart = ({ data, ticker, layout }) => {
  const chartContainerRef = useRef();

  useEffect(() => {
    if (!data || data.length === 0) return;

    const container = chartContainerRef.current;
    if (!container) return;

    const handleResize = () => {
      chart.applyOptions({ width: container.clientWidth });
    };

    const chart = createChart(container, {
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
        borderColor: '#2a2e39',
      },
    });

    const lineSeries = chart.addLineSeries({
      color: '#2962ff',
      lineWidth: 2,
      priceFormat: {
        type: 'price',
      },
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

    // data format: { time: '2022-01-01', value: 105, volume: 1000 }
    lineSeries.setData(data.map(d => ({
        time: d.time,
        value: d.value
    })));

    volumeSeries.setData(data.map(d => ({
        time: d.time,
        value: d.volume,
        color: '#26a69a44' // Single color for volume in line chart context or based on prev close
    })));

    chart.timeScale().fitContent();

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, ticker, layout]);

  return <div ref={chartContainerRef} style={{ width: '100%', height: '100%' }} />;
};

export default memo(PriceChart);
