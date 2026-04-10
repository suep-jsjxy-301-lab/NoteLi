import axios from 'axios';
import qs from 'qs';

export const loginApi = (username, password) => {
  const formData = qs.stringify({ username, password });
  
  return axios.post('/api/v1/auth/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
};

export const getMeApi = (token) => {
  return axios.get('/api/v1/user/me', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
};