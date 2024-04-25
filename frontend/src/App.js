import React from "react";
import './App.css';
import { Routes, Route, Link, BrowserRouter } from "react-router-dom";
import { MainPage } from './main';
import { RecommendPage } from "./recommend";
import { ForeignBookPage } from './foreign';
import NotFound from "./NotFound";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainPage/>}/>
          <Route path="/foreign" element={<ForeignBookPage/>}/>
          <Route path="/recommend" element={<RecommendPage/>}/>
          <Route path="*" element={<NotFound/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
