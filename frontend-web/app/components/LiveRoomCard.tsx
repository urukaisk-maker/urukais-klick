'use client'

interface LiveRoomCardProps {
  id: number
  title: string
  host: string
  listeners: number
  isLive: boolean
  onJoin: (roomId: number) => void
}

export default function LiveRoomCard({ id, title, host, listeners, isLive, onJoin }: LiveRoomCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition cursor-pointer border-2 border-transparent hover:border-indigo-500">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-red-500 to-pink-600 flex items-center justify-center text-white font-bold">
              {host.charAt(0).toUpperCase()}
            </div>
            {isLive && (
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white animate-pulse" />
            )}
          </div>
          <div>
            <h3 className="font-semibold text-gray-800">{title}</h3>
            <p className="text-gray-600 text-sm">por {host}</p>
          </div>
        </div>

        {isLive && (
          <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-semibold">
            🔴 EN VIVO
          </span>
        )}
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-gray-600">
          <span>👥</span>
          <span>{listeners} escuchando</span>
        </div>

        <button
          onClick={() => onJoin(id)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-full hover:bg-indigo-700 transition font-semibold"
        >
          Unirse
        </button>
      </div>
    </div>
  )
}
