import React,{ useState, useContext  } from 'react';
import logo from './images/logohome.png';
import { Container, Form, Button } from 'react-bootstrap';
import  { useNavigate} from 'react-router-dom'
import {AuthContext} from './AuthContext';
import axios from 'axios';
import './Login.css';

const Login = () => {
    // Inside your Login component
    const { setIsAuthenticated, setUser } = useContext(AuthContext);
    const [username, setUsername] = useState('');
    const [passw, setPassw] = useState('');
    const navigate = useNavigate();


    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const params = new URLSearchParams();
            params.append('username', username);
            params.append('passw', passw);
    
            // Make a POST request with the URLSearchParams object
            const res = await axios.post('/ntuaflix_api/login', params);
            
            const token = res.data.token;
           localStorage.setItem('token', token);
           localStorage.setItem('user', username); // Store the user inlocalStorage
            axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        
            // Validate the token by sending a request to a protected endpoint
            try {
            await axios.post('/ntuaflix_api/protected_endpoint', { token: token });
            setIsAuthenticated(true);
            setUser(username);
            navigate('/ntuaflix_api');
            } catch (err) {
            console.log('Token validation failed:', err);
           localStorage.removeItem('token');
            }
        } catch (err) {
            console.log('Login failed:', err);
            navigate('/ntuaflix_api/login');
        }
        };
       
    
    return (
        
        <div className="box" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh'}}>
            <div className="fadeIn" style={{ width: '400px'}}>
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                    <img src={logo} alt="Logo" style={{ width: '50%', height:'50%'}} />   
                </div>
                <Form onSubmit={handleSubmit}>
                    <Form.Group controlId="formBasicUser" >
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="user" placeholder="Enter Username" value={username} onChange={e => setUsername(e.target.value)} style={{ backgroundColor: '#555', color: '#fff' }}/>
                    </Form.Group>
    
                    <Form.Group controlId="formBasicPassword" style={{paddingTop:'1em'}}>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Password" value={passw} onChange={e => setPassw(e.target.value)} style={{ backgroundColor: '#555', color: '#fff' }}/>
                    </Form.Group>
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' , paddingTop:'1.3em'}}>
                        <Button variant="primary" type="submit" >
                            Login
                        </Button>
                    </div>
                </Form>
            </div>
        </div>
    
    );

}
export default Login;
