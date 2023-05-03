import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/itemslist.css';
import 'bootstrap/dist/css/bootstrap.min.css';


const Items = ({ categorySlug }) => {
  const [items, setItems] = useState([]);
  const [selectedItemId, setSelectedItemId] = useState(null);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const res = await axios.get(`http://192.168.7.221:8000/items/`);
        setItems(res.data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchItems();
  }, [categorySlug]);

  const handleItemClick = (itemId) => {
    setSelectedItemId(itemId);
  };



  return (
    <div className="container">
      <div className="row">
        {items.map((item) => (
          <div key={item.id} className="col-md-4 mb-4">
            <div className="box">
              <div className="image">
                <img src={item.image} alt={item.title} className="img-fluid" />
              </div>
              <div className="p-4">
                <h3>{item.title}</h3>
                <p className="text-color">{item.description}</p>
                <p>Price: {item.price}</p>
                <p>Instructions: {item.instructions}</p>
                <p>Labels: {item.labels}</p>
                <button className="button" onClick={() => handleItemClick(item.id)}>Details</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Items;
