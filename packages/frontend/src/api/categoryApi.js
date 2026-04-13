import request from './request';

const categoryApi = {

    getCategoriesApi() {
        return request.get('/category/list',{
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },
    
    createCategoryApi(categoryData) {
        return request.post('/category/create', categoryData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },
    
    deleteCategoryApi(id) {
        return request.post('/category/delete', { id }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

};

export default categoryApi;