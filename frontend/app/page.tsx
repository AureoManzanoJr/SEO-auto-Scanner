'use client'

import { useState } from 'react'
import { Search, Loader2, Download, Moon, Sun, TrendingUp, Link2, Image as ImageIcon, Smartphone, Zap } from 'lucide-react'
import axios from 'axios'

interface ScanResult {
  url: string
  timestamp: string
  score: number
  metadata: {
    title?: string
    description?: string
  }
  headings: {
    h1: string[]
    h2: string[]
  }
  links: {
    internal: string[]
    external: string[]
    broken: { url: string; status: string }[]
  }
  images: {
    total: number
    without_alt: number
  }
  performance?: {
    load_time: number
  }
  mobile_friendly: boolean
  sitemap?: string
  robots_txt?: string
}

export default function Home() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ScanResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [darkMode, setDarkMode] = useState(false)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  const handleScan = async () => {
    if (!url.trim()) {
      setError('Por favor, insira uma URL válida')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const normalizedUrl = url.startsWith('http') ? url : `https://${url}`
      const response = await axios.post(`${API_URL}/api/scan`, {
        url: normalizedUrl,
        depth: 1,
        include_external: false
      })

      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao realizar análise. Verifique se o backend está rodando.')
      console.error('Scan error:', err)
    } finally {
      setLoading(false)
    }
  }

  const downloadReport = async (format: 'html' | 'pdf' | 'json') => {
    if (!result) return

    try {
      const reportUrl = `${API_URL}/api/report/${format}?url=${encodeURIComponent(result.url)}`
      
      if (format === 'json') {
        const response = await axios.get(reportUrl)
        const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `seo-report-${result.url.replace(/https?:\/\//, '').replace(/\//g, '-')}.json`
        a.click()
      } else {
        window.open(reportUrl, '_blank')
      }
    } catch (err) {
      console.error('Download error:', err)
      alert('Erro ao baixar relatório')
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-500'
    if (score >= 60) return 'text-yellow-500'
    return 'text-red-500'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 dark:bg-green-900'
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900'
    return 'bg-red-100 dark:bg-red-900'
  }

  return (
    <div className={`min-h-screen transition-colors ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              🔍 SEO Auto Scanner
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Análise completa de SEO para seu site
            </p>
          </div>
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            aria-label="Toggle dark mode"
          >
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </header>

        {/* Search Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
          <div className="flex gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleScan()}
                placeholder="Digite a URL do site (ex: exemplo.com)"
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                disabled={loading}
              />
            </div>
            <button
              onClick={handleScan}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analisando...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Analisar
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded-lg mb-8">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Score Card */}
            <div className={`${getScoreBgColor(result.score)} rounded-lg shadow-lg p-8 text-center`}>
              <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
                Pontuação de SEO
              </h2>
              <div className={`text-7xl font-bold ${getScoreColor(result.score)} mb-2`}>
                {result.score}
              </div>
              <div className="text-gray-600 dark:text-gray-400 text-lg">
                de 100 pontos
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Link2 className="w-5 h-5 text-blue-500" />
                  <h3 className="font-semibold text-gray-700 dark:text-gray-300">Links Internos</h3>
                </div>
                <div className="text-3xl font-bold text-gray-900 dark:text-white">
                  {result.links.internal.length}
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div className="flex items-center gap-3 mb-2">
                  <ImageIcon className="w-5 h-5 text-purple-500" />
                  <h3 className="font-semibold text-gray-700 dark:text-gray-300">Imagens</h3>
                </div>
                <div className="text-3xl font-bold text-gray-900 dark:text-white">
                  {result.images.total}
                </div>
                {result.images.without_alt > 0 && (
                  <div className="text-sm text-red-500 mt-1">
                    {result.images.without_alt} sem ALT
                  </div>
                )}
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Zap className="w-5 h-5 text-yellow-500" />
                  <h3 className="font-semibold text-gray-700 dark:text-gray-300">Performance</h3>
                </div>
                <div className="text-3xl font-bold text-gray-900 dark:text-white">
                  {result.performance ? `${result.performance.load_time.toFixed(2)}s` : 'N/A'}
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Smartphone className="w-5 h-5 text-green-500" />
                  <h3 className="font-semibold text-gray-700 dark:text-gray-300">Mobile</h3>
                </div>
                <div className="text-3xl font-bold text-gray-900 dark:text-white">
                  {result.mobile_friendly ? '✓' : '✗'}
                </div>
              </div>
            </div>

            {/* Metadata */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Metadados</h2>
              <div className="space-y-3">
                {result.metadata.title && (
                  <div>
                    <div className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Título</div>
                    <div className="text-gray-900 dark:text-white">{result.metadata.title}</div>
                  </div>
                )}
                {result.metadata.description && (
                  <div>
                    <div className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Descrição</div>
                    <div className="text-gray-900 dark:text-white">{result.metadata.description}</div>
                  </div>
                )}
              </div>
            </div>

            {/* Headings */}
            {(result.headings.h1.length > 0 || result.headings.h2.length > 0) && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Estrutura de Headings</h2>
                {result.headings.h1.length > 0 && (
                  <div className="mb-4">
                    <div className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">H1 ({result.headings.h1.length})</div>
                    <ul className="list-disc list-inside space-y-1 text-gray-900 dark:text-white">
                      {result.headings.h1.map((h1, i) => (
                        <li key={i}>{h1}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {result.headings.h2.length > 0 && (
                  <div>
                    <div className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">H2 ({result.headings.h2.length})</div>
                    <ul className="list-disc list-inside space-y-1 text-gray-900 dark:text-white">
                      {result.headings.h2.slice(0, 10).map((h2, i) => (
                        <li key={i}>{h2}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Broken Links */}
            {result.links.broken.length > 0 && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4 text-red-600 dark:text-red-400">
                  Links Quebrados ({result.links.broken.length})
                </h2>
                <ul className="space-y-2">
                  {result.links.broken.map((link, i) => (
                    <li key={i} className="text-gray-900 dark:text-white">
                      {link.url}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Download Reports */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Baixar Relatórios</h2>
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={() => downloadReport('pdf')}
                  className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold flex items-center gap-2 transition-colors"
                >
                  <Download className="w-5 h-5" />
                  PDF
                </button>
                <button
                  onClick={() => downloadReport('html')}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold flex items-center gap-2 transition-colors"
                >
                  <Download className="w-5 h-5" />
                  HTML
                </button>
                <button
                  onClick={() => downloadReport('json')}
                  className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold flex items-center gap-2 transition-colors"
                >
                  <Download className="w-5 h-5" />
                  JSON
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-600 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700 pt-8">
          <p className="mb-2">
            Desenvolvido com ❤️ por{' '}
            <a
              href="https://iadev.pro"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:underline font-semibold"
            >
              Aureo Manzano Junior
            </a>
          </p>
          <p className="text-sm mb-2">
            <a
              href="mailto:aureomanzano@icloud.com"
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              aureomanzano@icloud.com
            </a>
            {' • '}
            <a
              href="https://iadev.pro"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              iadev.pro
            </a>
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-500">
            SEO Auto Scanner v1.0.0 • Open Source • MIT License
          </p>
        </footer>
      </div>
    </div>
  )
}

