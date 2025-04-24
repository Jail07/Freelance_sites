import React from "react";
import "./Gig.scss";
import { Slider } from "infinite-react-carousel/lib";
import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import newRequest from "../../utils/newRequest";
import Reviews from "../../components/reviews/Reviews";

function Gig() {
  const { id } = useParams();

  const { isLoading, error, data } = useQuery({
    queryKey: ["gig"],
    queryFn: () =>
      newRequest.get(`/projects/${id}`).then((res) => {
        return res.data;
      }),
  });

  const userId = data?.owner.id;

  const {
    isLoading: isLoadingUser,
    error: errorUser,
    data: dataUser,
  } = useQuery({
    queryKey: ["user"],
    queryFn: () =>
      newRequest.get(`/profiles/${userId}`).then((res) => {
        return res.data;
      }),
    enabled: !!userId,
  });

  return (
    <div className="gig">
      {isLoading ? (
        "loading"
      ) : error ? (
        "Something went wrong!"
      ) : (
        <div className="container">
          <div className="left">
            <span className="breadcrumbs">
              Fiverr {">"} Graphics & Design {">"}
            </span>
            <h1>{data.title}</h1>
            {isLoadingUser ? (
              "loading"
            ) : errorUser ? (
              "Something went wrong!"
            ) : (
                <div className="user">
                  <img
                    className="image"
                    src={`http://localhost:8000${dataUser.profile_image}`}
                    alt=""
                />
                  <span>{dataUser.name}</span>
                  {!isNaN(data.totalStars / data.starNumber) && (
                      <div className="stars">
                        {Array(Math.round(data.totalStars / data.starNumber))
                            .fill()
                            .map((item, i) => (
                                <img src="/img/star.png" alt="" key={i}/>
                            ))}
                        <span>{Math.round(data.totalStars / data.starNumber)}</span>
                      </div>
                  )}
                </div>
            )}
            <Slider slidesToShow={1} arrowsScroll={1} className="slider">
              <img
                  className="image"
                  src={`http://localhost:8000${data.featured_image}`}
                  alt={data.title}
              />
            </Slider>
            <h2>About This Gig</h2>
            <p>{data.description}</p>
            {isLoadingUser ? (
              "loading"
            ) : errorUser ? (
              "Something went wrong!"
            ) : (
              <div className="seller">
                <h2>About The Seller</h2>
                <div className="user">
                  <img
                      className="image"
                      src={`http://localhost:8000${dataUser.profile_image}`}
                      alt=""
                  />
                  <div className="info">
                    <span>{dataUser.name}</span>
                    {!isNaN(data.totalStars / data.starNumber) && (
                        <div className="stars">
                          {Array(Math.round(data.totalStars / data.starNumber))
                              .fill()
                              .map((item, i) => (
                                  <img src="/img/star.png" alt="" key={i}/>
                              ))}
                          <span>
                          {Math.round(data.totalStars / data.starNumber)}
                        </span>
                        </div>
                    )}
                    <button>Contact Me</button>
                  </div>
                </div>
                <div className="box">
                  <div className="items">
                    <div className="item">
                      <span className="title">From</span>
                      <span className="desc">{dataUser.location}</span>
                    </div>
                    <div className="item">
                      <span className="title">Member since</span>
                      <span className="desc">Aug 2022</span>
                    </div>
                    <div className="item">
                      <span className="title">Avg. response time</span>
                      <span className="desc">4 hours</span>
                    </div>
                    <div className="item">
                      <span className="title">Last delivery</span>
                      <span className="desc">1 day</span>
                    </div>
                    <div className="item">
                      <span className="title">Languages</span>
                      <span className="desc">English</span>
                    </div>
                  </div>
                  <hr />
                  <p>{dataUser.bio}</p>
                </div>
              </div>
            )}
            <Reviews gigId={id} />
          </div>
          <div className="right">
            <div className="price">
              <h3>{data.title}</h3>
              {/*<h2>$ {data.price}</h2>*/}
            </div>
            <p>{data.shortDesc}</p>
            <div className="details">
              <div className="item">
                <img src="/img/clock.png" alt="" />
                <span>{data.created} Days Delivery</span>
              </div>
              {/*<div className="item">*/}
              {/*  <img src="/img/recycle.png" alt="" />*/}
              {/*  <span>{data.revisionNumber} Revisions</span>*/}
              {/*</div>*/}
            </div>
            <div className="features">
              {data.tags.map((tags) => (
                <div className="item" key={tags.id}>
                  <img src="/img/greencheck.png" alt="" />
                  <span>{tags.name}</span>
                </div>
              ))}
            </div>
            <Link to={`/pay/${id}`}>
            <button>Continue</button>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export default Gig;
