import React,{useState,useContext,} from 'react';
import SearchContext from './SearchContext';
import logoimage from './images/logohome.png';
import { useNavigate } from 'react-router-dom';
import prof from 'bootstrap-icons/icons/person-circle.svg';
import './navbar.css'
import Logout from './Logout';
import { AuthContext } from './AuthContext';

function MyNavbar({ userName }){
    // const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();
    const [text, setText] = useState('');  // Local state for the input field
    const { setSearchTerm } = useContext(SearchContext);

    const { setIsAuthenticated } = useContext(AuthContext);

    const [isLoggingOut, setIsLoggingOut] = useState(false);

    const handleLogoutClick = () => {
        setIsLoggingOut(true);
    };
    const handleInputChange = (event) => {
        setText(event.target.value);  // Update the local state when the input field changes
    };
  
    const handleFormSubmit = async (event) => {
      event.preventDefault();

      setSearchTerm(text);  // Set the search results
      console.log(text);
    };
    const handleLogoClick = () => {
       setSearchTerm('');  // Reset the search results
        
       navigate('/ntuaflix_api') // Reset the search results
    }
  
  
    return (
        
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid" style={{ display: 'flex', justifyContent: 'center' }}>
                {/* <a className="navbar-brand" style={{color:"#BA0021"}} href="#">NTUAflix</a> */}
                <img className='navbar-brand' src={logoimage} onClick={handleLogoClick} alt="Logo" style={{ width: '4rem', height:'4rem'}} />
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent" style={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center' }}>
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                </ul>

                
                <form className="d-flex" role="search" onSubmit={handleFormSubmit}>
                    <input
                        className="form-control me-2 searchbar"
                        type="search"
                        placeholder = "Search"
                        aria-label="Search"
                        value={text}
                        onChange={handleInputChange}
                    />
                    {/* <img src={searchglass} className='searchglass' alt="search" style={{ width: '1.5rem', height:'1.5rem'}} /> */}
                    {/* <button className="btn btn-light btn-outline-success" onClick={handleFormSubmit} type="submit"> <img src={searchglass} className='searchglass' alt="search" style={{ width: '1.5rem', height:'1.5rem'}} /></button> */}
                </form>
                <ul className="navbar-nav" style={{padding:'1rem'}}>
                
                <img src={prof} className='prof' alt="search" style={{ width: '1.5rem', height:'1.5rem',  color: "white",marginTop:"0.5rem"}} />
                <h5 style={{ color: 'white', marginLeft:"1rem" ,marginTop:"0.5rem"}}>{userName}</h5>
                <button className='btn btn-danger' onClick={handleLogoutClick}  style={{marginLeft:"1rem"}}>Logout</button>
                {isLoggingOut && <Logout />}
                </ul>
                </div>
            </div>
        </nav>
    );
    

}

export default MyNavbar;