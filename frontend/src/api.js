const API_URL = import.meta.env.VITE_API_URL || '/api'

async function request(path, options = {}) {
  const token = localStorage.getItem('booking_token')
  const headers = new Headers(options.headers || {})
  if (options.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Token ${token}`)

  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  const data = await response.json().catch(() => ({}))

  if (response.status === 401) {
    localStorage.removeItem('booking_token')
    window.dispatchEvent(new Event('booking-auth-expired'))
    throw new Error(data.detail || 'Your session has expired. Please log in again.')
  }

  if (!response.ok) {
    const detail = data.detail || data.error || Object.values(data).flat?.().join(' ') || 'Something went wrong'
    throw new Error(detail)
  }
  return data
}

export const api = {
  rooms: () => request('/rooms/'),
  room: (id) => request(`/rooms/${id}/`),
  occupancies: () => request('/occupancies/'),
  createOccupancy: (payload) => request('/occupancies/', { method: 'POST', body: JSON.stringify(payload) }),
  register: (payload) => request('/register/', { method: 'POST', body: JSON.stringify(payload) }),
  login: (payload) => request('/login/', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request('/logout/', { method: 'POST' }),
}
