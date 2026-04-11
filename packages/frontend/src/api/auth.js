import axios from 'axios';
import qs from 'qs';

const request = axios.create({
  baseURL: '/api/v1'
});

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const loginApi = (username, password) => {
  const formData = qs.stringify({ username, password });
  
  return axios.post('/api/v1/auth/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
};

export const getMeApi = (token) => {
  return request.get('/user/me', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
};

export const registerApi = (payload) => {
  return request.post('/user/register', payload, {
    headers: {
      'Content-Type': 'application/json'
    }
  });
};

export const verify_password = (password) => {
  return request.post('/auth/verify-password', { password }, {
    headers: {
      'Content-Type': 'application/json'
    }
  });
};

export const logoutApi = (refresh_token, access_token) => {
  return request.post('/auth/logout', { refresh_token }, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${access_token}`
    }
  });
}

export const deleteMeApi = () => {
  return request.post('/user/delete');
}

export const changePasswordApi = (new_password) => {
  return request.post('/user/change-password', { new_password }, {
    headers: {
      'Content-Type': 'application/json'
    }
  });
}