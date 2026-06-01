'use client'

import { useState } from 'react'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import DiscoveryFeed from './components/DiscoveryFeed'
import SocialWall from './components/SocialWall'
import LiveRooms from './components/LiveRooms'
import AudioPlayer from './components/AudioPlayer'

export default function Home() {
  const [view, setView] = useState<'login' | 'register' | 'home' | 'discovery' | 'social' | 'live'>('login')
  const [currentTrack, setCurrentTrack] = useState<any>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Datos de ejemplo (simulados)
  const [tracks] = useState([
    { id: 1, title: 'Ecos de la Noche', artist: 'Luna Solitaria', cover_url: '', duration: 245, klick_count: 42 },
    { id: 2, title: 'Ritmo Urbano', artist: 'Callejero Beats', cover_url: '', duration: 198, klick_count: 38 },
    { id: 3, title: 'Melancolía Azul', artist: 'Sombra Eterna', cover_url: '', duration: 312, klick_count: 55 },
  ])

  const [posts] = useState([
    { id: 1, user: 'Melómano', content: 'Hoy me siento nostálgico, escuchando viejos clásicos 📻', mood: 'nostalgic', reactions: 12 },
    { id: 2, user: 'MusicLover', content: '¡Acabo de descubrir a este artista increíble! 🎵', track: { title: 'Ecos de la Noche', artist: 'Luna Solitaria' }, reactions: 8 },
  ])

  const [rooms] = useState([
    { id: 1, title: 'Jazz Session Nocturna', host: 'SaxMaster', current_listeners: 24, is_active: true },
    { id: 2, title: 'Indie Discovery Hour', host: 'CuradorMusical', current_listeners: 18, is_active: true },
  ])

  const handleLogin = (email: string, password: string) => {
    // Simular login
    setIsAuthenticated(true)
    setView('home')
  }

  const handleRegister = (alias: string, email: string, password: string) => {
    // Simular registro
    setIsAuthenticated(true)
    setView('home')
  }

  const handleAnonymous = () => {
    setIsAuthenticated(true)
    setView('home')
  }

  const handlePlayTrack = (id: number) => {
    const track = tracks.find(t => t.id === id)
    if (track) {
      setCurrentTrack(track)
    }
  }

  const handleKlickTrack = (id: number) => {
    // Simular Klick
    console.log('Klick enviado para pista:', id)
  }

  const handleReactPost = (postId: number) => {
    // Simular reacción
    console.log('Reacción enviada para post:', postId)
  }

  const handleCreatePost = (content: string, trackId?: number, mood?: string) => {
    // Simular creación de post
    console.log('Post creado:', content)
  }

  const handleJoinRoom = (roomId: number) => {
    // Simular unirse a sala
    console.log('Uniéndose a sala:', roomId)
  }

  const handleCreateRoom = (title: string, description: string) => {
    // Simular creación de sala
    console.log('Sala creada:', title)
  }

  if (!isAuthenticated) {
    if (view === 'register') {
      return <RegisterForm onRegister={handleRegister} onBack={() => setView('login')} />
    }
    return <LoginForm onLogin={handleLogin} onRegister={() => setView('register')} onAnonymous={handleAnonymous} />
  }

  return (
    <main className="min-h-screen">
      {/* Header */}
      <header className="glass-effect sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-3xl font-bold gradient-text">Urukais Klick</h1>
          <nav className="flex gap-2">
            <button onClick={() => setView('home')} className={`px-6 py-2 rounded-full transition-all duration-300 ${view === 'home' ? 'btn-gradient text-white' : 'text-white hover:bg-white/20'}`}>Inicio</button>
            <button onClick={() => setView('discovery')} className={`px-6 py-2 rounded-full transition-all duration-300 ${view === 'discovery' ? 'btn-gradient text-white' : 'text-white hover:bg-white/20'}`}>Descubrir</button>
            <button onClick={() => setView('social')} className={`px-6 py-2 rounded-full transition-all duration-300 ${view === 'social' ? 'btn-gradient text-white' : 'text-white hover:bg-white/20'}`}>Social</button>
            <button onClick={() => setView('live')} className={`px-6 py-2 rounded-full transition-all duration-300 ${view === 'live' ? 'btn-gradient text-white' : 'text-white hover:bg-white/20'}`}>Live</button>
          </nav>
        </div>
      </header>

      {/* Content */}
      <div className="p-4 pb-32">
        {view === 'home' && (
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-5xl font-bold text-white mb-4">Bienvenido a Urukais Klick</h2>
              <p className="text-xl text-white/80">Descubre música, conecta con artistas y apoya el talento</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              <div className="glass-effect p-8 rounded-2xl card-hover">
                <div className="text-4xl mb-4">🎯</div>
                <h3 className="text-2xl font-bold text-white mb-3">Descubre</h3>
                <p className="text-white/80">Música personalizada basada en tus emociones</p>
              </div>
              <div className="glass-effect p-8 rounded-2xl card-hover">
                <div className="text-4xl mb-4">👥</div>
                <h3 className="text-2xl font-bold text-white mb-3">Conecta</h3>
                <p className="text-white/80">Salas en directo y comunidad</p>
              </div>
              <div className="glass-effect p-8 rounded-2xl card-hover">
                <div className="text-4xl mb-4">👏</div>
                <h3 className="text-2xl font-bold text-white mb-3">Apoya</h3>
                <p className="text-white/80">Klicks gratuitos a tus artistas</p>
              </div>
            </div>
            <DiscoveryFeed tracks={tracks} onPlayTrack={handlePlayTrack} onKlickTrack={handleKlickTrack} />
          </div>
        )}

        {view === 'discovery' && (
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl font-bold text-white mb-8 text-center">Descubrir Música</h2>
            <DiscoveryFeed tracks={tracks} onPlayTrack={handlePlayTrack} onKlickTrack={handleKlickTrack} />
          </div>
        )}

        {view === 'social' && (
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl font-bold text-white mb-8 text-center">Comunidad</h2>
            <SocialWall posts={posts} onReact={handleReactPost} onCreatePost={handleCreatePost} />
          </div>
        )}

        {view === 'live' && (
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl font-bold text-white mb-8 text-center">Salas en Directo</h2>
            <LiveRooms rooms={rooms} onJoinRoom={handleJoinRoom} onCreateRoom={handleCreateRoom} />
          </div>
        )}
      </div>

      {/* Audio Player Fixed */}
      {currentTrack && (
        <div className="fixed bottom-0 left-0 right-0 glass-effect border-t border-white/20">
          <div className="max-w-7xl mx-auto p-4">
            <AudioPlayer
              audioUrl={currentTrack.audio_url || ''}
              title={currentTrack.title}
              artist={currentTrack.artist}
              coverUrl={currentTrack.cover_url}
              onKlick={() => handleKlickTrack(currentTrack.id)}
            />
          </div>
        </div>
      )}
    </main>
  )
}
