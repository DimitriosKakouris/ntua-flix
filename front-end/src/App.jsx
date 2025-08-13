import User from "./user";
import Home from "./Home";
import Login from "./Login";
import SelectedMovie from "./selectedMovie";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import React, { useState } from "react";
import { AuthContext } from "./AuthContext";
import SearchContext from "./SearchContext";
import RedirectToNtuaflixApi from "./redirect";
import Logout from "./Logout";
import axios from "axios";
import { useEffect } from "react";
import SearchResults from "./SearchHome";

const App = () => {
  useEffect(() => {
    const handleTabClose = (event) => {
      event.preventDefault();
      axios({
        method: "get",
        url: "/logout",
        async: false,
      });
    };

    window.addEventListener("beforeunload", handleTabClose);

    return () => {
      window.removeEventListener("beforeunload", handleTabClose);
    };
  }, []);

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [user, setUser] = useState(null);

  return (
    <SearchContext.Provider value={{ searchTerm, setSearchTerm }}>
      <AuthContext.Provider
        value={{ isAuthenticated, setIsAuthenticated, user, setUser }}
      >
        {
          <Router>
            <Routes>
              <Route path="/" element={<RedirectToNtuaflixApi />} />
              <Route path="/ntuaflix_api" element={<Home />} />
              <Route
                path="/ntuaflix_api/search/:searchterm"
                element={<SearchResults />}
              />
              <Route path="/ntuaflix_api/login" element={<Login />} />
              <Route path="/ntuaflix_api/logout" element={<Logout />} />
              <Route
                path="/ntuaflix_api/admin/healthcheck"
                element={<User />}
              />
              <Route
                path="/ntuaflix_api/admin/upload/titlebasics"
                element={<User />}
              />
              <Route
                path="/ntuaflix_api/admin/upload/titleakas"
                element={<User />}
              />
              <Route
                path="/ntuaflix_api/admin/upload/titlecrew"
                element={<User />}
              />
              <Route
                path="/ntuaflix_api/admin/upload/titleepisode"
                element={<User />}
              />
              <Route
                path="/ntuaflix_api/admin/upload/titleprincipals"
                element={<User />}
              />
              <Route
                path="/ntuaflix_api/admin/upload/titleratings"
                element={<User />}
              />
              <Route
                path="/ntuaflix_api/movie/:titleID"
                element={<SelectedMovie />}
              />
              <Route path="/ntuaflix_api/user" element={<User />} />
              <Route path="/ntuaflix_api/title/:titleID" element={<User />} />
              <Route
                path="/ntuaflix_api/searchtitle/<title>"
                element={<User />}
              />
              <Route path="/ntuaflix_api/bygenre" element={<User />} />
              <Route path="/ntuaflix_api/name/<nameID>" element={<User />} />
              <Route
                path="/ntuaflix_api/searchname/<nameID>"
                element={<User />}
              />
            </Routes>
          </Router>
        }
      </AuthContext.Provider>
    </SearchContext.Provider>
  );
};

export default App;
