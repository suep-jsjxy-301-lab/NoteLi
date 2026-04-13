import qs from 'qs';
import request from './request';

const UserApi = {
    
    loginApi(username, password) {
        const formData = qs.stringify({ username, password });
        return request.post('/auth/token', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
    },

    getMeApi(token) {
        return request.get('/user/me', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
    },

    registerApi(payload) {
        return request.post('/user/register', payload, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },
    verify_passwordApi(password) {
        return request.post('/auth/verify-password', { password }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },

    logoutApi(refresh_token, access_token) {
        return request.post('/auth/logout', { refresh_token }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            }
        });
    },

    deleteMeApi() {
        return request.post('/user/delete');
    },

    changePasswordApi(new_password) {
        return request.post('/user/change-password', { new_password }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },

    changeEmailApi(new_email) {
        return request.post('/user/change-email', { new_email }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },

    changePhoneApi(new_phone) {
        return request.post('/user/change-phone', { new_phone }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },

    changeUserNameApi(new_username) {
        return request.post('/user/change-username', { new_username }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
};

export default UserApi;