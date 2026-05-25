import userApi from '@/api/userApi';
import categoryApi from '@/api/categoryApi';
import noteApi from '@/api/noteApi';
import agentApi from '@/api/agentApi';

const Api = {
    user: userApi,
    category: categoryApi,
    note: noteApi,
    agent: agentApi,
};
export default Api;