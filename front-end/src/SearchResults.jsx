import { useParams } from 'react-router-dom';
import React,{ useContext, useEffect,useState } from 'react';
import MyNavbar from './navbar';
import SearchContext from './SearchContext';
import { useNavigate } from 'react-router-dom';
import {AuthContext}  from './AuthContext';
import axios from 'axios';
import MovieList from './movielist';

function SearchResults() {
    const { searchTerm } = useContext(SearchContext);
    const [searchedMovies, setSearchedMovies] = useState([]);
    const { isAuthenticated, user } = useContext(AuthContext);
    const navigate = useNavigate();

 

    useEffect(() => {
      const fetchMoviesSearch = async () => {
        const res1 = await axios.post(`/ntuaflix_api/searchtitlealias`, 
          { titlePart: searchTerm },  // Request body
          { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }
        );
    
        const res2 = await axios.post(`/ntuaflix_api/bygenrealias`, 
          { qgenre: searchTerm},  // Request body
          { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }
        );
      
        const dat1 = res1.data;
        const dat2 = res2.data;
        console.log(dat2);
    
        const movies1 = Object.values(dat1);  // Get the results from the first endpoint
        const movies2 = Object.values(dat2);  // Get the results from the second endpoint
    
        const tconsts1 = movies1.map(movie => movie.tconst); // Get the tconsts from the movie objects
        const tconsts2 = movies2.map(movie => movie.tconst); // Get the tconsts from the movie objects
    
        const combinedTconsts = tconsts1.concat(tconsts2);  // Combine the tconsts
    
        setSearchedMovies(combinedTconsts);  // Update the state with the fetched data
      };
    
      fetchMoviesSearch();
    
      
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
            <MovieList seenMoviesList={searchedMovies} />
        </div>
    );
}

export default SearchResults;