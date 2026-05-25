import request from './request'

const agentApi = {

    processMessageApi(Message) {
        return request.post('/chat/message', { message: Message }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
}

export default agentApi;