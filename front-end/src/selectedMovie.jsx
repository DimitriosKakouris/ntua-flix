import React, { useContext, useState, useEffect } from 'react';
import { Toast } from 'react-bootstrap';
import { Typography } from '@mui/material';
import { Rating } from '@mui/material';
import MyNavbar from './navbar';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';
import axios from 'axios';
import MovieList from './movielist';
import './selectedMovie.css';

function SelectedMovie() {
    const { isAuthenticated, user } = useContext(AuthContext);

    const navigate = useNavigate();
    const [selectedOption, setSelectedOption] = useState(0);
    const [showToast, setShowToast] = useState(false);
    const [showToastNot, setShowToastNot] = useState(false);
    const [flag, setFlag] = useState('');
    const [actors, setActors] = useState([]);
    const [crew, setCrew] = useState([]);
    const { titleID } = useParams(); // Get the titleID from the URL parameters
    const [moviedetails, setMovieDetails] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const response = await axios.get(`/ntuaflix_api/title/${titleID}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = response.data;
            handleMovieDetails(data);
            handleActorsAndCrew(data);
        };
    
        fetchData();
    }, [titleID]);
    
    const handleMovieDetails = async (data) => {
        let movieDetails = {
            title: data.originalTitle,
            type: data.type ? data.type : 'n/a',
            startYear: data.startYear,
            genres: data.genres ? data.genres.join(', ') : 'n/a',
            ratings: data.rating ? data.rating.avrating : 'n/a',
        };
    
        if(movieDetails.type === 'tvEpisode') {
            const response = await axios.get(`/ntuaflix_api/tvepisode/${titleID}`)
            const data = response.data;
            console.log(data);
            movieDetails = {
                ...movieDetails,
                season: data.season ,
                episode: data.episode
            };
        }
    
        setMovieDetails(movieDetails);
    }
    
    const handleActorsAndCrew = (data) => {
        const actors_list = data.principals.filter(person => person.category === 'actor' || person.category === 'actress');
        const crew_list = data.principals.filter(person => person.category !== 'actor' && person.category !== 'actress');
        setActors(actors_list);
        setCrew(crew_list);
    }

  



    const handleVote = () => {
       
        axios.post('/ntuaflix_api/vote', {
            titleID: titleID,
            rating: selectedOption,
        }, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then(function (response) {
            if (response.data.flag === 1) {
                console.log('Already Voted');
                setShowToastNot(true);
                
            }
            else{
                setShowToast(true);
            }
        });
       
    };


    useEffect(() => {
        const checkSeenMovies = async () => {
            if (!isAuthenticated) {
                navigate('/ntuaflix_api/login');
            } else {
                try {
                    const response = await fetch(`/ntuaflix_api/seenmovies`,
                    {
                        headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                      });
                    const data = await response.json();
                    console.log(data);
                  
                    if (data.includes(titleID)) {
                        console.log('seen');
                        setFlag('seen');
                    } else {
                        console.log('not seen');
                        setFlag('notSeen');
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        };

        checkSeenMovies();
    }, [isAuthenticated, navigate, titleID]);

    if (flag === 'seen') {
        return (
            <div className="SelectedMovie">
                <MyNavbar userName={user} />
                <div className="main" style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <div style={{ flex: '1' }}>
                        <MovieList seenMoviesList={[titleID]} />
                    </div>

                    <div
                        className="card text-center fadeInUp"
                        style={{
                            flex: '1',
                            marginLeft: '7rem',
                            marginRight: '7rem',
                            marginTop: '4rem',
                            marginBottom: '9rem',
                            height: '40vh',
                            backgroundColor: '#77767b',
                            color: 'white',
                            borderRadius: '3%',
                            boxShadow: '0 10px 10px 5px rgba(0,0,0,0.2)',
                        }}
                    >
                        <div className="card-body">
                            <h5 className="card-title">Rate this Title</h5>

                            <div className="rating" style={{ marginTop: '2rem' }}>
                                <Typography component="legend"></Typography>
                                <Rating name="customized-10" defaultValue={0} max={10} onChange={(event, newValue) => {setSelectedOption(newValue);}} />
                            </div>
                        </div>

                        <div className="card-footer text-muted">
                            <button onClick={handleVote} id="liveToastBtn" className="btn btn-primary">
                                Vote
                            </button> 

                        </div>
                        
                    </div>
                    
                </div>
                <Toast style={{ position: 'absolute', bottom: 20, right: 20, minWidth: '200px'}}onClose={() => setShowToastNot(false)} show={showToastNot} delay={3000} autohide>
                            <Toast.Header>
                                <strong className="me-auto">NTUAflix</strong>
                                <small>1 sec ago</small>
                            </Toast.Header>
                            <Toast.Body>You can not vote (already voted or undefined rating)!</Toast.Body>
                </Toast>
                <Toast style={{ position: 'absolute', bottom: 20, right: 20, minWidth: '200px'}}onClose={() => setShowToast(false)} show={showToast} delay={3000} autohide>
                            <Toast.Header>
                                <strong className="me-auto">NTUAflix</strong>
                                <small>1 sec ago</small>
                            </Toast.Header>
                            <Toast.Body>Thank you for your vote!</Toast.Body>
                </Toast>
            </div>
        );
    } else {
        return (
            <div className="SelectedMovie">
                <MyNavbar userName={user} />
                <div className="main" style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <div style={{ flex: '1' }}>
                        <MovieList seenMoviesList={[titleID]} />
                    </div>
    
                <div style={{ flex: '1', display: 'flex', flexDirection: 'column', gap: '1rem', marginLeft: '8rem', marginTop: '2rem',}}>
                <div
                    className="card text-center fadeInUp"
                    style={{
                       
                        backgroundColor: '#77767b',
                        color: 'white',
                        borderRadius: '3%',
                        height: '330px',
                       
                        boxShadow: '0 10px 10px 5px rgba(0,0,0,0.2)',
                        overflow: 'auto',
                    }}
                >   
               
                    <div className="card-body" style={{backgroundColor: '#970404'}}>
                        <h5 className="card-title">Movie Details</h5>
                        <p className="card-text">Title: {moviedetails.title}</p>
                        <p className="card-text">Type: {moviedetails.type}</p>
                        {moviedetails.type === 'tvEpisode' ? (
                        <>
                            <p className="card-text">Season: {moviedetails.season}</p>
                            <p className="card-text">Episode: {moviedetails.episode}</p>
                        </>
                    ) : null}
                        <p className="card-text">Year: {moviedetails.startYear}</p>
                        <p className="card-text">Genre: {moviedetails.genres}</p>
                        <p className="card-text">Rating: {moviedetails.ratings}</p>
                    </div>
                </div>
                </div>
                <div style={{ flex: '1', display: 'flex', flexDirection: 'column', gap: '1rem', marginLeft: '1rem', marginRight: '1rem', marginTop: '2rem',  }}>

                <div
                    className="card text-center fadeInUp"
                    style={{
                       
                        backgroundColor: '#77767b',
                        color: 'white',
                        borderRadius: '3%',
                        height: '200px',
                      
                        boxShadow: '0 10px 10px 5px rgba(0,0,0,0.2)',
                        overflow: 'auto',
                    }}
                >
                    <div className="card-body">
                        <h5 className="card-title">Actors/Actresses</h5>
                        {actors.map(actor => (
                            <p className="card-text">{actor.name}</p>
                        ))}
                    </div>
                </div>

                <div
                    className="card text-center fadeInUp"
                    style={{
                      
                        backgroundColor: '#77767b',
                        color: 'white',
                        borderRadius: '3%',
                        height: '300px',
                      
                        boxShadow: '0 10px 10px 5px rgba(0,0,0,0.2)',
                        overflow: 'auto',
                    }}
                >
                    <div className="card-body">
                        <h5 className="card-title">Crew</h5>
                        {crew.map(crewMember => (
                            <p className="card-text">{crewMember.category}: {crewMember.name}</p>
                        ))}
                    </div>
                </div>
            </div>
            </div>
            </div>
        );
    }
}

export default SelectedMovie;
