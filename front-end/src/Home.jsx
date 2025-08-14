import React,{ useContext, useEffect,useState } from 'react';
import MyNavbar from './navbar';

import { useNavigate } from 'react-router-dom';
import {AuthContext}  from './AuthContext';
import SearchContext from './SearchContext';
import MovieList from './movielist';

function Home() {
  
    const { isAuthenticated, user } = useContext(AuthContext);
    const { searchTerm } = useContext(SearchContext);
    
    
    const [seenMoviesList, setSeenMoviesList] = useState([]);
    const [searchedMovies, setSearchedMovies] = useState([]);
    const navigate = useNavigate();
    
    
    useEffect(() => {
      const fetchseenMoviesList = async () => {
        const res = await fetch(`/ntuaflix_api/seenmovies/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });

        const dat = await res.json();
        console.log(dat);
      
  
        setSeenMoviesList(dat);  // Update the state with the fetched data
      }
    const fetchMoviesSearch = async () => {
      console.log("Here")
      const res = await fetch(`/ntuaflix_api/searchtitle/${searchTerm}`,  
      {
        headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      } );
      const dat = await res.json();
      console.log(dat); 
      const movies = Object.values(dat);  // Get the results
      // console.log(movies);
      // const tconsts = movies.map(movie => movie.tconst); // Get the tconsts from the search results
      // console.log(tconsts);
    
      const tconsts = movies.map(movie => movie.tconst); // Get the tconsts from the movie objects
      console.log(tconsts); 
      setSearchedMovies(tconsts);  // Update the state with the fetched data

    };

    if (isAuthenticated) {
      fetchseenMoviesList();
      if (searchTerm) navigate(`/ntuaflix_api/search/${searchTerm}`);
    } else {
      navigate('/ntuaflix_api/login');
    }
    // Cleanup function
    return () => {
      setSearchedMovies([]);  // Reset the search results
  };
  },[isAuthenticated, user, searchTerm, navigate]);  // Dependency array

  
    // Filter seenMoviesList based on searchTerm before passing it to MovieList
    const filteredMoviesList = searchedMovies.length > 0 ? searchedMovies : seenMoviesList;

    return (
      <div className="Home" style={{'backgroundColor':'#393939', 'color':'white'}}>
        <MyNavbar userName={user} />
        {searchedMovies.length === 0 && <h4 style={{marginLeft:"3rem", marginTop:"1rem"}}>My Titles</h4>}
        <MovieList seenMoviesList={filteredMoviesList} gridnum={8} />
      </div>
    );
}


export default Home;
