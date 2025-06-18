import type { Metadata } from 'next'
import Header from '../components/Header'
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
      <body>
        <Header />
        <main className="main-content">
          {children}
        </main>
      </body>
    </html>
  )
}
