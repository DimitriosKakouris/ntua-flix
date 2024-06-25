import React from 'react';

export const AuthContext = React.createContext({
  isAuthenticated: false,
  user: null,
  isLoading: true,
  // Any other values or functions you want to provide
});