import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SEO Auto Scanner - Análise Completa de SEO',
  description: 'Ferramenta profissional para análise automática de SEO de qualquer site. Desenvolvido por Aureo Manzano Junior.',
  keywords: 'SEO, análise SEO, scanner SEO, otimização, SEO tools, Aureo Manzano Junior, iadev.pro',
  authors: [{ name: 'Aureo Manzano Junior', url: 'https://iadev.pro' }],
  creator: 'Aureo Manzano Junior',
  publisher: 'Aureo Manzano Junior',
  openGraph: {
    title: 'SEO Auto Scanner - Análise Completa de SEO',
    description: 'Ferramenta profissional para análise automática de SEO',
    url: 'https://github.com/AureoManzanoJr/SEO-auto-Scanner',
    siteName: 'SEO Auto Scanner',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SEO Auto Scanner',
    description: 'Ferramenta profissional para análise automática de SEO',
    creator: '@AureoManzanoJr',
  },
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="canonical" href="https://github.com/AureoManzanoJr/SEO-auto-Scanner" />
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  )
}

