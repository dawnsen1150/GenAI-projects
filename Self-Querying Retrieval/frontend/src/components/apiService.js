const fetchSimilarItems = async (description,accessToken) => {
    const payload = { text: description};
  
    try {
      const response = await fetch('/api/similar_items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`
        },
        body: JSON.stringify(payload),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("API Response:", data);
        return data;
      } else {
        console.error("API Error:", response.statusText);
        throw new Error(response.statusText);
      }
    } catch (error) {
      console.error("Fetch Error:", error);
      throw error;
    }
};

export default fetchSimilarItems