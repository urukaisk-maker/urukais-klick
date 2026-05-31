'use client'

import { useState } from 'react'

interface RegisterFormProps {
  onRegister: (alias: string, email: string, password: string) => void
  onBack: () => void
}

export default function RegisterForm({ onRegister, onBack }: RegisterFormProps) {
  const [alias, setAlias] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [step, setStep] = useState(1) // 1: datos básicos, 2: ruleta de estados

  const moods = [
    { id: 'happy', emoji: '😊', name: 'Feliz' },
    { id: 'sad', emoji: '😢', name: 'Triste' },
    { id: 'energetic', emoji: '⚡', name: 'Energético' },
    { id: 'relaxed', emoji: '😌', name: 'Relajado' },
    { id: 'romantic', emoji: '💕', name: 'Romántico' },
    { id: 'focused', emoji: '🎯', name: 'Concentrado' },
    { id: 'nostalgic', emoji: '📻', name: 'Nostálgico' },
    { id: 'adventurous', emoji: '🌍', name: 'Aventurero' },
  ]

  const [selectedMoods, setSelectedMoods] = useState<string[]>([])

  const toggleMood = (moodId: string) => {
    if (selectedMoods.includes(moodId)) {
      setSelectedMoods(selectedMoods.filter(m => m !== moodId))
    } else if (selectedMoods.length < 3) {
      setSelectedMoods([...selectedMoods, moodId])
    }
  }

  const handleBasicSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (alias && email && password) {
      setStep(2)
    }
  }

  const handleMoodSubmit = () => {
    if (selectedMoods.length > 0) {
      onRegister(alias, email, password)
    }
  }

  if (step === 1) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Crear Cuenta</h1>
            <p className="text-gray-600">Únete a Urukais Klick</p>
          </div>

          <form onSubmit={handleBasicSubmit} className="space-y-4">
            <div>
              <label htmlFor="alias" className="block text-sm font-medium text-gray-700 mb-1">
                Alias
              </label>
              <input
                type="text"
                id="alias"
                value={alias}
                onChange={(e) => setAlias(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Tu nombre de usuario"
                required
              />
            </div>

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
              Continuar →
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={onBack}
              className="text-gray-600 hover:text-gray-800"
            >
              ← Volver
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">¿Cómo te sientes?</h1>
          <p className="text-gray-600">Selecciona hasta 3 estados de ánimo (seleccionados: {selectedMoods.length}/3)</p>
        </div>

        <div className="grid grid-cols-4 gap-3 mb-6">
          {moods.map((mood) => (
            <button
              key={mood.id}
              onClick={() => toggleMood(mood.id)}
              className={`p-4 rounded-xl text-center transition ${
                selectedMoods.includes(mood.id)
                  ? 'bg-indigo-600 text-white scale-105'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              <div className="text-3xl mb-1">{mood.emoji}</div>
              <div className="text-xs">{mood.name}</div>
            </button>
          ))}
        </div>

        <button
          onClick={handleMoodSubmit}
          disabled={selectedMoods.length === 0}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition font-semibold disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Completar Registro
        </button>

        <div className="mt-4 text-center">
          <button
            onClick={() => setStep(1)}
            className="text-gray-600 hover:text-gray-800"
          >
            ← Atrás
          </button>
        </div>
      </div>
    </div>
  )
}
