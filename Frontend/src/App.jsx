import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
  const [news, setNews] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/news") // Replace with your backend API
      .then((response) => setNews(response.data))
      .catch((error) => console.error("Error fetching news:", error));
  }, []);

  return (
    <div className="min-h-screen min-w-screen flex flex-col bg-white overflow-hidden">
      
      {/* Navbar */}
      <div className="navbar bg-base-100">
  <a className="btn btn-ghost text-xl">Know It All</a>
</div>
<div
  className="hero size-70"
  style={{
    backgroundImage: "url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.webp)",
  }}>
  <div className="hero-overlay bg-opacity-60"></div>
  <div className="hero-content text-neutral-content text-center">
    <div className="max-w-md">
      <h1 className="mb-5 text-5xl font-bold">Hello there</h1>
      <p className="mb-5">
        Stay up to date in this fast paced world with us!
      </p>
      
    </div>
  </div>
</div>

      {/* News Grid */}
      <div className="container mx-auto p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 flex-grow">
        {news.map((article, index) => (
          <div key={index} className="bg-white p-4 rounded-lg shadow-lg">
            <img src={article.image_url} alt={article.headline} className="w-full h-40 object-cover rounded-md" />
            <h2 className="text-gray-900 font-extrabold mt-2">{article.headline}</h2>
            <p className="text-gray-600 text-sm">{article.summary}</p>
            <a href={article.source_link} target="_blank" rel="noopener noreferrer" className="text-blue-500 mt-2 inline-block">Read More</a>
          </div>
        ))}
      </div>

      {/* Footer */}
      <footer className="footer footer-center bg-base-300 text-base-content p-4">
  <aside>
    <p>Copyright © {new Date().getFullYear()} - All right reserved by Know It All</p>
  </aside>
</footer>
    </div>
  );
};

export default App;
