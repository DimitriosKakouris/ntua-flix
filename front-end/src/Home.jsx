import React,{ useContext, useEffect,useState } from 'react';
import MyNavbar from './navbar';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {AuthContext}  from './AuthContext';
import SearchContext from './SearchContext';
import MovieList from './movielist';
import './scrollbar.css';

function Home() {
  
    const { isLoading,isAuthenticated, user} = useContext(AuthContext);
    const { searchTerm } = useContext(SearchContext);
    
    
    const [seenMoviesList, setSeenMoviesList] = useState([]);
    const [searchedMovies, setSearchedMovies] = useState([]);
    const navigate = useNavigate();
  
    
    useEffect(() => {
      const fetchseenMoviesList = async () => {
        const res = await axios.get(`/ntuaflix_api/seenmovies`);
        const dat = res.data;
        console.log(dat);

        if (dat === null) {
          // The response is empty
          setSeenMoviesList([]);  // Set the state to an empty array
        }
        else{
        setSeenMoviesList(dat);  // Update the state with the fetched data
      }
      }
      
  
   
  const fetchData = async () => {
  
    if (!isLoading) {
      if (isAuthenticated) {
        await fetchseenMoviesList();
        if (searchTerm) navigate(`/ntuaflix_api/search/${searchTerm}`);
      } else {
        navigate('/ntuaflix_api/login');
      }
    }
  }


  fetchData();

    // Cleanup function
    return () => {
      setSearchedMovies([]);  // Reset the search results
  };
  },[isLoading,isAuthenticated, user, searchTerm, navigate]);  // Dependency array

  if (isLoading) {
    return <div>Loading...</div>; // or some loading spinner
  }

  
    // Filter seenMoviesList based on searchTerm before passing it to MovieList
    const filteredMoviesList = searchedMovies.length > 0 ? searchedMovies : seenMoviesList;

    return (
      <div className="Home" style={{'backgroundColor':'#393939', 'color':'white'}}>
        <MyNavbar userName={user} />
        {searchedMovies.length === 0 && <h4 style={{marginLeft:"3rem", marginTop:"1rem"}}>My Titles</h4>}
        <MovieList seenMoviesList={filteredMoviesList} />
      </div>
    );
}


export default Home;
