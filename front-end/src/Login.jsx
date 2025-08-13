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

    const handleSubmit = async (event) => {
        event.preventDefault();

        // const response = await fetch('/login', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({ username, password })
        // });

        // const data = await response.json();

        axios.post('/ntuaflix_api/login', { username, passw })
        .then(response => {
            localStorage.setItem('token', response.data.token);
            setIsAuthenticated(true);
            setUser(username);
            console.log("Success");
            navigate('/ntuaflix_api');
        })
        .catch(error => {
            console.error('There was an error!', error);
            navigate('/ntuaflix_api/login');
        });
     


        // if (response.status === 200) {
        //     setIsAuthenticated(true);
        //     setUser(data.user);  // set the user data
        //     // Redirect the user
        //     navigate('/');
        // } else {
        //     // Show an error message
        //     console.error(data.msg);
        //     navigate('/login');
        // }
        // console.log(data);
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
