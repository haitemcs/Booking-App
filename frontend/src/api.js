const API_URL = import.meta.env.VITE_API_URL || '/api'

async function request(path, options = {}) {
  const token = localStorage.getItem('booking_token')
  const headers = new Headers(options.headers || {})
  headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Token ${token}`)

  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.detail || data.error || 'Something went wrong')
  }
  return data
}

export const api = {
  rooms: () => request('/rooms/'),
  room: (id) => request(`/rooms/${id}/`),
  occupancies: () => request('/occupancies/'),
  createOccupancy: (payload) => request('/occupancies/', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
  register: (payload) => request('/register/', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
  login: (payload) => request('/login/', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
  logout: () => request('/logout/', { method: 'POST' }),
}
