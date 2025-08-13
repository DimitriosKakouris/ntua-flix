import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Logout() {
  const navigate = useNavigate();
  async function logout() {
   
    await fetch('/ntuaflix_api/logout', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    window.close();
  }
  useEffect(() => {
    logout();
    navigate('/ntuaflix_api/login');
  }, []);
  return null;
}