import { useParams } from 'react-router-dom';
import React,{ useContext, useEffect,useState } from 'react';
import MyNavbar from './navbar';
import SearchContext from './SearchContext';
import { useNavigate } from 'react-router-dom';
import {AuthContext}  from './AuthContext';

import MovieList from './movielist';

function SearchResults() {
    const { searchTerm } = useContext(SearchContext);
    const [searchedMovies, setSearchedMovies] = useState([]);
    const { isAuthenticated, user } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
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
            // const tconsts = movies.map(movie => movie.tconst); // Get the tconsts from the movie objects
            // console.log(tconsts); 
            setSearchedMovies(dat);  // Update the state with the fetched data
      
          };
      
          if (isAuthenticated) {
            fetchMoviesSearch();
        } else {
          navigate('/ntuaflix_api/login');
        }
        // Cleanup function
        return () => {
          setSearchedMovies([]);  // Reset the search results
      };
      },[isAuthenticated, user, searchTerm, navigate]);  // Dependency array
    

    return (
        <div className="SearchResults" style={{'backgroundColor':'#393939', 'color':'white'}}>
            <MyNavbar userName={user} />
            <h4 style={{marginLeft:"3rem", marginTop:"1rem"}}>Search Results for "{searchTerm}"</h4>
            <MovieList seenMoviesList={searchedMovies} gridnum={8}/>
        </div>
    );
}

export default SearchResults;