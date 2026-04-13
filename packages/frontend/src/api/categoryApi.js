import request from './request';

const categoryApi = {

    getCategoriesApi() {
        return request.get('/category/list',{
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },
    
    createCategoryApi(category_icon, category_name) {
        return request.post('/category/create', { category_icon, category_name }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    },
    
    deleteCategoryApi(category_name) {
        return request.post('/category/delete', { category_name }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

};

export default categoryApi;