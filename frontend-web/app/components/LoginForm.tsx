'use client'

import { useState } from 'react'

interface LoginFormProps {
  onLogin: (email: string, password: string) => void
  onRegister: () => void
  onAnonymous: () => void
}

export default function LoginForm({ onLogin, onRegister, onAnonymous }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onLogin(email, password)
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="glass-effect rounded-3xl shadow-2xl p-8 w-full max-w-md card-hover">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold gradient-text mb-2">Urukais Klick</h1>
          <p className="text-white/80 text-lg">Descubrimiento musical gratuito</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-white mb-2">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:ring-2 focus:ring-white/50 focus:border-transparent text-white placeholder-white/50 backdrop-blur-sm"
              placeholder="tu@email.com"
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-white mb-2">
              Contraseña
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:ring-2 focus:ring-white/50 focus:border-transparent text-white placeholder-white/50 backdrop-blur-sm"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full btn-gradient text-white py-3 rounded-xl font-semibold text-lg"
          >
            Iniciar Sesión
          </button>
        </form>

        <div className="mt-8 space-y-4">
          <button
            onClick={onAnonymous}
            className="w-full bg-white/10 text-white py-3 rounded-xl hover:bg-white/20 transition font-semibold border border-white/20 backdrop-blur-sm"
          >
            🎲 Entrar como Anónimo
          </button>

          <div className="text-center">
            <span className="text-white/80">¿No tienes cuenta?</span>
            <button
              onClick={onRegister}
              className="text-white font-semibold ml-1 hover:underline"
            >
              Regístrate
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
