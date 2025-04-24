import React from "react";
import "./GigCard.scss";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import newRequest from "../../utils/newRequest";

const GigCard = ({ item }) => {
  const { isLoading, error, data } = useQuery({
    queryKey: [item.owner.id],
    queryFn: () =>
      newRequest.get(`/profiles/${item.owner.id}/`).then((res) => {
        console.log(res.data)
        return res.data;
      }),
  });
  return (
    <Link to={`/gig/${item.id}`} className="link">
      <div className="gigCard">
        <img
            className="image"
            src={`http://localhost:8000${item.featured_image}`}
            alt={item.title}
        />
        <div className="info">
          {isLoading ? (
              "loading"
          ) : error ? (
              "Something went wrong!"
          ) : (
              <div className="user">
                <img
                    className="image"
                    src={`http://localhost:8000${item.featured_image}`}
                    alt={item.title}
                />
                <span>{item.title}</span>
              </div>
          )}
          <p>{item.description}</p>
          <div className="star">
            <img src="./img/star.png" alt=""/>
            <span>
              {!isNaN(item.totalStars / item.starNumber) &&
                  Math.round(item.totalStars / item.starNumber)}
            </span>
          </div>
        </div>
        <hr/>
        <div className="detail">
          <img src="./img/heart.png" alt=""/>
          <div className="price">
            <span>STARTING AT</span>
            <h2>??? $</h2>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default GigCard;
