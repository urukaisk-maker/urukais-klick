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
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="glass-effect rounded-3xl shadow-2xl p-8 w-full max-w-md card-hover">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold gradient-text mb-2">Crear Cuenta</h1>
            <p className="text-white/80 text-lg">Únete a Urukais Klick</p>
          </div>

          <form onSubmit={handleBasicSubmit} className="space-y-6">
            <div>
              <label htmlFor="alias" className="block text-sm font-medium text-white mb-2">
                Alias
              </label>
              <input
                type="text"
                id="alias"
                value={alias}
                onChange={(e) => setAlias(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:ring-2 focus:ring-white/50 focus:border-transparent text-white placeholder-white/50 backdrop-blur-sm"
                placeholder="Tu nombre de usuario"
                required
              />
            </div>

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
              Continuar →
            </button>
          </form>

          <div className="mt-8 text-center">
            <button
              onClick={onBack}
              className="text-white/80 hover:text-white transition"
            >
              ← Volver
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="glass-effect rounded-3xl shadow-2xl p-8 w-full max-w-md card-hover">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold gradient-text mb-2">¿Cómo te sientes?</h1>
          <p className="text-white/80 text-lg">Selecciona hasta 3 estados de ánimo (seleccionados: {selectedMoods.length}/3)</p>
        </div>

        <div className="grid grid-cols-4 gap-3 mb-6">
          {moods.map((mood) => (
            <button
              key={mood.id}
              onClick={() => toggleMood(mood.id)}
              className={`p-4 rounded-xl text-center transition-all duration-300 ${
                selectedMoods.includes(mood.id)
                  ? 'btn-gradient text-white scale-110 shadow-lg'
                  : 'bg-white/10 hover:bg-white/20 text-white border border-white/20 backdrop-blur-sm'
              }`}
            >
              <div className="text-3xl mb-1">{mood.emoji}</div>
              <div className="text-xs font-medium">{mood.name}</div>
            </button>
          ))}
        </div>

        <button
          onClick={handleMoodSubmit}
          disabled={selectedMoods.length === 0}
          className="w-full btn-gradient text-white py-3 rounded-xl font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          Completar Registro
        </button>

        <div className="mt-6 text-center">
          <button
            onClick={() => setStep(1)}
            className="text-white/80 hover:text-white transition"
          >
            ← Atrás
          </button>
        </div>
      </div>
    </div>
  )
}
