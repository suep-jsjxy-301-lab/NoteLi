import request from '@/api/request';
import userApi from '@/api/userApi';
import categoryApi from '@/api/categoryApi';
import qs from 'qs';


const Api = {
    user: userApi,
    category: categoryApi
};
export default Api;