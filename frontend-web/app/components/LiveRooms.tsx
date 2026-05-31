'use client'

import { useState } from 'react'
import LiveRoomCard from './LiveRoomCard'

interface Room {
  id: number
  title: string
  host: string
  current_listeners: number
  is_active: boolean
}

interface LiveRoomsProps {
  rooms: Room[]
  onJoinRoom: (roomId: number) => void
  onCreateRoom: (title: string, description: string) => void
}

export default function LiveRooms({ rooms, onJoinRoom, onCreateRoom }: LiveRoomsProps) {
  const [showCreate, setShowCreate] = useState(false)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  const handleCreate = () => {
    if (title.trim()) {
      onCreateRoom(title, description)
      setTitle('')
      setDescription('')
      setShowCreate(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Salas en Directo</h2>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-full hover:bg-indigo-700 transition"
        >
          + Crear Sala
        </button>
      </div>

      {showCreate && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h3 className="font-semibold mb-4">Crear Nueva Sala</h3>
          <div className="space-y-4">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Título de la sala"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Descripción (opcional)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              rows={2}
            />
            <div className="flex gap-2">
              <button
                onClick={handleCreate}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
              >
                Crear
              </button>
              <button
                onClick={() => setShowCreate(false)}
                className="px-6 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {rooms.map((room) => (
          <LiveRoomCard
            key={room.id}
            id={room.id}
            title={room.title}
            host={room.host}
            listeners={room.current_listeners}
            isLive={room.is_active}
            onJoin={onJoinRoom}
          />
        ))}
      </div>

      {rooms.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg">No hay salas activas</p>
          <p className="text-gray-400 text-sm mt-2">Crea una sala o espera a que alguien inicie una</p>
        </div>
      )}
    </div>
  )
}
