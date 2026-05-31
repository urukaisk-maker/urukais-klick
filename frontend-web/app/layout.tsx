import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Urukais Klick - Descubrimiento Musical Gratuito',
  description: 'Plataforma gratuita de descubrimiento musical y conexión artística',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
