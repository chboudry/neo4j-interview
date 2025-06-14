import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Neo4j Interview App',
  description: 'Neo4j Interview Project Frontend',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
