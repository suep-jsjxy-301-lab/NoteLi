import axios from 'axios';
import qs from 'qs';

export const loginApi = (username, password) => {
  const formData = qs.stringify({ username, password });
  
  return axios.post('/auth/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
};