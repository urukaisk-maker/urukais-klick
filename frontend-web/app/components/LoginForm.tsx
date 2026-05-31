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
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Urukais Klick</h1>
          <p className="text-gray-600">Descubrimiento musical gratuito</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="tu@email.com"
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Contraseña
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition font-semibold"
          >
            Iniciar Sesión
          </button>
        </form>

        <div className="mt-6 space-y-3">
          <button
            onClick={onAnonymous}
            className="w-full bg-gray-100 text-gray-700 py-3 rounded-lg hover:bg-gray-200 transition font-semibold"
          >
            🎲 Entrar como Anónimo
          </button>

          <div className="text-center">
            <span className="text-gray-600">¿No tienes cuenta?</span>
            <button
              onClick={onRegister}
              className="text-indigo-600 font-semibold ml-1 hover:underline"
            >
              Regístrate
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
