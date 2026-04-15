import userApi from '@/api/userApi';
import categoryApi from '@/api/categoryApi';
import noteApi from '@/api/noteApi';

const Api = {
    user: userApi,
    category: categoryApi,
    note: noteApi
};
export default Api;