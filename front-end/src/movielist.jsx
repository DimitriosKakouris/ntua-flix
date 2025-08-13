import React, { useEffect, useState } from 'react';
import placeholderImage from './images/logo.png';
import Bistar  from 'bootstrap-icons/icons/star-fill.svg';
import './movielist.css';
import { useNavigate } from 'react-router-dom';



function MovieList({ seenMoviesList},{flag}) {
    const [movies, setMovies] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
        let seenMoviesArray = seenMoviesList;
        console.log(seenMoviesList);
        if (typeof seenMoviesList === 'string') {
            seenMoviesArray = seenMoviesList.split(',');
        }
        fetchMovies(seenMoviesArray);
    }, [seenMoviesList])
    
    const fetchMovies = async (seenMoviesArray) => {
        const movies = [];
        
        for (const id of seenMoviesArray) {
            try {
                const response = await fetch(`/ntuaflix_api/title/${id}`,
                {
                    headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                  } );
                console.log(response);
                const data = await response.json();
    
                // const mappedData = {
                //     id: data.title_basics._id,
                //     title: data.title_basics.originalTitle,
                //     img: data.title_basics.img_url_asset,
                //     genres: data.title_basics.genres,
                //     ratings: data.title_ratings.avrating,
                //     tconst: data.title_basics.tconst
                // };
                const mappedData = {
                    id: data.title_basics.imdb_id,
                    title: data.title_basics.original_title,
                    // img: data.title_basics.img_url_asset,
                    img: "http://image.tmdb.org/t/p/w500/"+data.title_basics.poster_path,
                    genres: data.title_genre,
                    ratings: data.title_ratings.avrating,
                  
                };
    
    
                movies.push(mappedData);
                console.log(movies);
            } catch (error) {
                console.log(error);
            }
        }
    
        setMovies(movies);
    

    };
    function Handlemovieselection(tconst) {
        console.log(tconst);
      
        navigate(`/ntuaflix_api/movie/${tconst}`);
    };
    
    return (
        
        <div style={{ 
            display: "flex", 
            flexWrap: "wrap",
            justifyContent: "space-around",
            alignItems: "stretch",
            alignContent: "flex-start",  // Align the cards to the top of the container
            overflowY: 'scroll',
            height: '90vh',
            paddingLeft:"2em",
            paddingRight:"2em",
            paddingTop:"1em",
            paddingBottom:"2em"
        }}>
        {movies.map(movie => (
            <div className="card fadeInFromBelow" style={{ width: '14.1rem', margin:"2em", border: '1px solid #333333', borderRadius: '3%',boxShadow: '0 10px 10px 5px rgba(0,0,0,0.2)'  }}>
          <img 
                src={movie.img !== "\\N" ? movie.img.replace('{width_variable}', 'w342') : placeholderImage} 
                alt={movie.title}  
                style={{height:"281.2px", width:"224px"}}
            />
            <div className="card-body" style={{backgroundColor: "#141715"}}>
            <a className="card-title" onClick={() => Handlemovieselection(movie.id)} style={{
                textDecoration:"none",
                    color: 'white', 
                    overflow: 'hidden',  // Hide the overflow
                    textOverflow: 'ellipsis',  // Add an ellipsis when the text overflows
                    // whiteSpace: 'nowrap' , // Prevent the text from wrapping onto multiple lines
                    maxWidth: '100%',
                }}>{movie.title}</a>
                <div style={{color:"white"}}>
                <p className="card-text">Genre: {movie.genres}</p>
                </div>
            </div>
            <div className="card-footer" style={{alignItems:"center"}}>
            
                <h6 className="list-group-item" style={{marginLeft:"2rem",marginRight:"2rem"}}> <img src={Bistar} className='bistar' alt="search" style={{ width: '1.5rem', height:'1.5rem',  marginRight:'1rem'}} /><span >Rating: {movie.ratings}</span></h6>
                
            
            </div>
            {/* <div className="card-body">
                <a href="#" className="card-link">Card link</a>
                <a href="#" className="card-link">Another link</a>
            </div> */}
            </div>
        )
        )}
        </div>
        )
       
  
        }
export default MovieList;