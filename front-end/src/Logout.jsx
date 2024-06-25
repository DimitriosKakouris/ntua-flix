import { useContext, useEffect } from 'react';
import axios from 'axios';
import { AuthContext } from './AuthContext';

function Logout() {
  const { setIsAuthenticated } = useContext(AuthContext);

  useEffect(() => {
    const logout = async () => {
      try {
        await axios.post('/ntuaflix_api/logout');
        localStorage.removeItem('token');
        setIsAuthenticated(false);
      } catch (error) {
        console.error('Failed to log out:', error);
      }
    };

    logout();
  }, [setIsAuthenticated]);

  return null;
}

export default Logout;