import Home from './Home';
import Login from './Login';
import SelectedMovie from './selectedMovie';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import React, { useState, useEffect} from 'react';
import {AuthContext} from './AuthContext';
import RedirectToNtuaflixApi from './redirect';
import SearchContext from './SearchContext';
import SearchResults from './SearchResults';
import ProtectedRoute from './protected'; 
import axios from 'axios';

function App() {
  

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
 
  const [user, setUser] = useState(null);

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.post('/ntuaflix_api/protected_endpoint', { token: token }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
        .then(response => {
          if (response.status === 200) {
            setIsAuthenticated(true);
          } else {
            setIsAuthenticated(false);
          }
        })
        .catch(error => {
          setIsAuthenticated(false);
        });
    }
    setIsLoading(false);
  }, []);
 
   
  return (  
    <SearchContext.Provider value={{ searchTerm, setSearchTerm }}>
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, user, setUser }}>{
    <Router>
        <Routes>
        <Route path="/" element={<RedirectToNtuaflixApi />} />
        <Route path="/ntuaflix_api" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/ntuaflix_api/search/:searchterm" element={<ProtectedRoute><SearchResults /></ProtectedRoute>} />
        <Route path="/ntuaflix_api/login" element={<Login/>} />
        <Route path="/ntuaflix_api/selectedtitle/:titleID" element={<ProtectedRoute><SelectedMovie /></ProtectedRoute>} />
          {/* <Route path="/ntuaflix_api/user" element={<User />} />
          <Route path='/ntuaflix_api/title/:titleID' element={<User />} />
          <Route path='/ntuaflix_api/searchtitle/<title>' element={<User />} />
          <Route path='/ntuaflix_api/bygenre' element={<User />} />
          <Route path='/ntuaflix_api/name/<nameID>' element={<User />} />
          <Route path='/ntuaflix_api/searchname/<nameID>' element={<User />} /> */}
        </Routes>
      </Router>
}
    </AuthContext.Provider>
    </SearchContext.Provider>
    
    
  
  );
}

export default App;

