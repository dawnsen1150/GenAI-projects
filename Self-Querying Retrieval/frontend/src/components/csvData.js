import React from 'react';
import useAuth from '../hooks/useAuth';

const downloadData = async (api) => 
    {
        const headers = [
          "Item Number", "Color", "Depth (cm)", "Height (cm)", 
          "Width (cm)", "Price (\$)", "Style", "Type","image"
        ];
        
        const csvData = api.map(item => [
          item.metadata.item_number,
          item.metadata.color,
          item.metadata.depth,
          item.metadata.height,
          item.metadata.width,
          item.metadata.price,
          item.metadata.style,
          item.metadata.type,
          item.metadata.url
        ]);
        
        csvData.unshift(headers);
        
        const csvContent = csvData.map(row => row.join(',')).join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        if (link.download !== undefined) {
          const url = URL.createObjectURL(blob);
          link.setAttribute("href", url);
          link.setAttribute("download", "similar_items_data.csv");
          link.style.visibility = 'hidden';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }
      }

export default downloadData