import { useEffect, useMemo, useState } from 'react'
import { api } from './api'

function todayString() {
  const date = new Date()
  const offset = date.getTimezoneOffset()
  return new Date(date.getTime() - offset * 60 * 1000).toISOString().slice(0, 10)
}

function App() {
  const [rooms, setRooms] = useState([])
  const [bookings, setBookings] = useState([])
  const [view, setView] = useState('home')
  const [selectedRoom, setSelectedRoom] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [authOpen, setAuthOpen] = useState(false)
  const [authMode, setAuthMode] = useState('login')
  const [loggedIn, setLoggedIn] = useState(Boolean(localStorage.getItem('booking_token')))

  const availableRooms = useMemo(() => rooms.filter((room) => room.is_available), [rooms])

  async function loadRooms() {
    setLoading(true)
    setError('')
    try {
      const data = await api.rooms()
      setRooms(data.results || data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function loadBookings() {
    try {
      const data = await api.occupancies()
      setBookings(data.results || data)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => { loadRooms() }, [])
  useEffect(() => {
    const handleExpired = () => {
      setLoggedIn(false)
      setView('home')
      setAuthOpen(false)
      setError('Your session has expired. Please log in again.')
    }
    window.addEventListener('booking-auth-expired', handleExpired)
    return () => window.removeEventListener('booking-auth-expired', handleExpired)
  }, [])
  useEffect(() => { if (loggedIn && view === 'bookings') loadBookings() }, [loggedIn, view])

  function openRoom(room) {
    setSelectedRoom(room)
    setView('details')
  }

  function handleAuth(result) {
    localStorage.setItem('booking_token', result.token)
    setLoggedIn(true)
    setAuthOpen(false)
    setError('')
  }

  async function handleLogout() {
    try { await api.logout() } catch { /* local logout still happens */ }
    localStorage.removeItem('booking_token')
    setLoggedIn(false)
    setView('home')
    setBookings([])
  }

  return (
    <div className="app-shell">
      <header className="navbar">
        <button className="brand" onClick={() => setView('home')}>StayEasy</button>
        <nav>
          <button className={view === 'home' ? 'nav-link active' : 'nav-link'} onClick={() => setView('home')}>Rooms</button>
          {loggedIn && <button className={view === 'bookings' ? 'nav-link active' : 'nav-link'} onClick={() => setView('bookings')}>My bookings</button>}
          {loggedIn ? (
            <button className="button secondary small" onClick={handleLogout}>Log out</button>
          ) : (
            <button className="button small" onClick={() => { setAuthMode('login'); setAuthOpen(true) }}>Log in</button>
          )}
        </nav>
      </header>

      <main>
        {error && <div className="alert">{error}<button onClick={() => setError('')}>×</button></div>}

        {view === 'home' && (
          <>
            <section className="hero">
              <div>
                <p className="eyebrow">ROOM BOOKING</p>
                <h1>Find a room that fits your stay.</h1>
                <p className="hero-copy">Simple booking, clear prices, and comfortable rooms.</p>
              </div>
              <div className="hero-card"><span>Available rooms</span><strong>{availableRooms.length}</strong></div>
            </section>
            <section className="section">
              <div className="section-heading"><div><p className="eyebrow">OUR ROOMS</p><h2>Choose your room</h2></div></div>
              {loading ? <div className="empty">Loading rooms…</div> : availableRooms.length === 0 ? <div className="empty">No rooms are currently available.</div> : (
                <div className="room-grid">
                  {availableRooms.map((room) => <RoomCard key={room.url || room.room_number} room={room} onClick={() => openRoom(room)} />)}
                </div>
              )}
            </section>
          </>
        )}

        {view === 'details' && selectedRoom && (
          <RoomDetails room={selectedRoom} loggedIn={loggedIn} onBack={() => setView('home')} onLogin={() => { setAuthMode('login'); setAuthOpen(true) }} onBooked={() => { setView('bookings'); setLoggedIn(true); loadBookings() }} />
        )}

        {view === 'bookings' && (
          <section className="section narrow"><p className="eyebrow">ACCOUNT</p><h1>My bookings</h1>
            {bookings.length === 0 ? <div className="empty">You have no bookings yet.</div> : <div className="booking-list">{bookings.map((booking) => <div className="booking-row" key={booking.id}><div><strong>Room</strong><span>{typeof booking.room === 'string' ? booking.room.split('/').filter(Boolean).pop() : booking.room}</span></div><div><strong>Check-in</strong><span>{booking.start_date}</span></div><div><strong>Check-out</strong><span>{booking.end_date}</span></div></div>)}</div>}
          </section>
        )}
      </main>

      {authOpen && <AuthModal mode={authMode} onClose={() => setAuthOpen(false)} onSuccess={handleAuth} onModeChange={setAuthMode} />}
    </div>
  )
}

function RoomCard({ room, onClick }) {
  const image = room.images?.[0]?.image
  return <article className="room-card" onClick={onClick}>
    <div className="room-image">{image ? <img src={image} alt={`Room ${room.room_number}`} /> : <span>{room.room_type}</span>}</div>
    <div className="room-content"><div className="room-title"><h3>{room.room_type}</h3><strong>{room.price_per_night} {room.currency}<small>/ night</small></strong></div><p>Room {room.room_number}</p><p className="description">{room.description || 'A comfortable room for your stay.'}</p><button className="text-button">View room →</button></div>
  </article>
}

function RoomDetails({ room, loggedIn, onBack, onLogin, onBooked }) {
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const image = room.images?.[0]?.image

  async function book(e) {
    e.preventDefault(); setSaving(true); setMessage('')
    try {
      await api.createOccupancy({ room: room.url, start_date: start, end_date: end })
      setMessage('Booking confirmed.')
      setTimeout(onBooked, 600)
    } catch (err) {
      setMessage(err.message)
    } finally {
      setSaving(false)
    }
  }

  return <section className="details">
    <button className="back" onClick={onBack}>← Back to rooms</button>
    <div className="details-grid"><div className="details-image">{image ? <img src={image} alt={`Room ${room.room_number}`} /> : <span>{room.room_type}</span>}</div>
      <div className="details-copy"><p className="eyebrow">ROOM {room.room_number}</p><h1>{room.room_type}</h1><p className="price">{room.price_per_night} {room.currency}<small> / night</small></p><p>{room.description || 'A comfortable room for your stay.'}</p>
        {loggedIn ? <form className="booking-form" onSubmit={book}><label>Check-in<input type="date" required min={todayString()} value={start} onChange={(e) => { setStart(e.target.value); if (end && e.target.value >= end) setEnd('') }} /></label><label>Check-out<input type="date" required min={start || todayString()} value={end} onChange={(e) => setEnd(e.target.value)} /></label><button className="button" disabled={saving}>{saving ? 'Booking…' : 'Book this room'}</button>{message && <p className="form-message">{message}</p>}</form> : <div className="login-prompt"><p>Log in to book this room.</p><button className="button" onClick={onLogin}>Log in</button></div>}
      </div></div>
  </section>
}

function AuthModal({ mode, onClose, onSuccess, onModeChange }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [email, setEmail] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function submit(e) {
    e.preventDefault()
    setError('')
    if (mode === 'register' && password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }
    setBusy(true)
    try {
      const result = mode === 'login'
        ? await api.login({ username, password })
        : await api.register({ username, password, email })
      onSuccess(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return <div className="modal-backdrop" onClick={onClose}><div className="modal" onClick={(e) => e.stopPropagation()}><button className="modal-close" onClick={onClose}>×</button><p className="eyebrow">ACCOUNT</p><h2>{mode === 'login' ? 'Welcome back' : 'Create your account'}</h2><form onSubmit={submit}><label>Username<input required value={username} onChange={(e) => setUsername(e.target.value)} /></label>{mode === 'register' && <label>Email<input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} /></label>}<label>Password<input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} /></label>{mode === 'register' && <label>Confirm password<input type="password" required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} /></label>}{error && <p className="form-error">{error}</p>}<button className="button full" disabled={busy}>{busy ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Create account'}</button></form><p className="switch-auth">{mode === 'login' ? 'New here?' : 'Already have an account?'} <button onClick={() => { setError(''); setConfirmPassword(''); onModeChange(mode === 'login' ? 'register' : 'login') }}>{mode === 'login' ? 'Create an account' : 'Log in'}</button></p></div></div>
}

export default App
