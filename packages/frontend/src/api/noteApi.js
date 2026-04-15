import request from './request'

const noteApi = {
  createNoteApi(payload) {
    return request.post('/note/create', payload, {
      headers: { 'Content-Type': 'application/json' },
    })
  },
  listNotesApi() {
    return request.get('/note/list', {
      headers: { 'Content-Type': 'application/json' },
    })
  },
  updateNoteApi(payload) {
    return request.post('/note/update', payload, {
      headers: { 'Content-Type': 'application/json' },
    })
  },
  deleteNoteApi(id) {
    return request.post('/note/delete', { id }, {
      headers: { 'Content-Type': 'application/json' },
    })
  },
  updateNoteStarredApi(payload) {
    return request.post('/note/update_starred', payload, {
      headers: { 'Content-Type': 'application/json' },
    })
  },
}

export default noteApi