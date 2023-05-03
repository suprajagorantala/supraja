import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "../styles/itemslist.css"

const ItemDetail = ({ itemId }) => {
    const [item, setItem] = useState(null);
    const [review, setReview] = useState("");
    const [reviews, setReviews] = useState([]);

    const handleReviewSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post(`http://192.168.7.221:8000/reviews/`, {
                item: itemId,
                review: review,
            });
            setReviews([...reviews, res.data]);
            setReview("");
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        const fetchItem = async () => {
            try {
                const res = await axios.get(`http://192.168.7.221:8000/items/${itemId}/`);
                setItem(res.data);
            } catch (error) {
                console.error(error);
            }
        };
        const fetchReviews = async () => {
            try {
                const res = await axios.get(`http://192.168.7.221:8000/items/${itemId}/reviews/`);
                setReviews(res.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchItem();
        fetchReviews();
    }, [itemId]);

    if (!item) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h3>{item.title}</h3>
            <p>{item.description}</p>
            <p>Price: {item.price}</p>
            <p>Instructions: {item.instructions}</p>
            <img src={item.image} alt={item.title} />
            <p>Labels: {item.labels}</p>

            <h4>Reviews:</h4>
            <ul>
                {reviews.map((review) => (
                    <li key={review.id}>{review.review}</li>
                ))}
            </ul>

            <form onSubmit={handleReviewSubmit}>
                <label>
                    Review:
                    <input type="text" value={review} onChange={(e) => setReview(e.target.value)} />
                </label>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default ItemDetail;
