import { useState } from 'react'
import './App.css'
import fetchSimilarItems from './components/apiService'
import downloadData from './components/csvData'
import useAuth from './hooks/useAuth'

function App() {
  const { isAuthenticated,user,token } = useAuth();
  const [description,setDescription]=useState('')
  const [apiResponse,setApiResponse]=useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const data = await fetchSimilarItems(description,token);
      setApiResponse(data);
    } 
    catch (error) {
      console.error("Fetch Error:", error);
      setApiResponse(error);
    }
  };

  const handleDownload = async (event) => {
    event.preventDefault();
    if (apiResponse && Array.isArray(apiResponse)) {
      try {
        downloadData(apiResponse);
      } 
      catch (error) {
        console.error("Fetch Error:", error);
      }
    }
  };

  return (
    <>
      <h2>Similar Product Search</h2>
      <form className='main-content' onSubmit={handleSubmit}>
        <input type='text' placeholder='Enter Product Descriptions'
        value={description} onChange={(e)=>setDescription(e.target.value)}/>
        <button type='submit' className='submit-button'>Submit</button>
      </form>

      {apiResponse && Array.isArray(apiResponse) && (
        <button onClick={handleDownload} className='download-button'>Download CSV</button>
      )}

      <div className="response">
        {apiResponse ? (
          Array.isArray(apiResponse) ? (
            <div className="result-gallery">
              {apiResponse.map((item, index) => (
                <div key={index} className="item-container">
                  <img src={item.metadata.url} alt="Item image" className="item-image" />
                  <div className="item-details">
                    <p><strong>Item Number:</strong> {item.metadata.item_number}</p>
                    <p><strong>Color:</strong> {item.metadata.color}</p>
                    <p><strong>Depth:</strong> {item.metadata.depth} cm</p>
                    <p><strong>Height:</strong> {item.metadata.height} cm</p>
                    <p><strong>Width:</strong> {item.metadata.width} cm</p>
                    <p><strong>Price:</strong> ${item.metadata.price}</p>
                    <p><strong>Style:</strong> {item.metadata.style}</p>
                    <p><strong>Type:</strong> {item.metadata.type}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="error">{apiResponse.error}</div>
          )
        ) : (
          <div></div>
        )}
      </div>
    </>
  )
}

export default App;
