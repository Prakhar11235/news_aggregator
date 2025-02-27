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
    <div className="min-h-screen w-screen flex flex-col">
      {/* Navbar */}
      <nav className="bg-blue-600 p-4 text-white text-lg font-bold text-center">
        News Aggregator
      </nav>

      {/* News Grid */}
      <div className="container mx-auto p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 flex-grow">
        {news.map((article, index) => (
          <div key={index} className="bg-white p-4 rounded-lg shadow-lg">
            <img src={article.image_url} alt={article.headline} className="w-full h-40 object-cover rounded-md" />
            <h2 className="text-gray-900 font-bold mt-2">{article.headline}</h2>
            <p className="text-gray-600 text-sm">{article.summary}</p>
            <a href={article.source_link} target="_blank" rel="noopener noreferrer" className="text-blue-500 mt-2 inline-block">Read More</a>
          </div>
        ))}
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white text-center p-4 mt-6">
        &copy; {new Date().getFullYear()} News Aggregator | All rights reserved
      </footer>
    </div>
  );
};

export default App;
