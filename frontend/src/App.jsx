import { useEffect, useState } from 'react'
import { obtenerEstadoApi } from './api/cliente.js'

export default function App() {
  const [estado, setEstado] = useState(null)
  const [error, setError] = useState(null)
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    obtenerEstadoApi()
      .then(setEstado)
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false))
  }, [])

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6">
      <section className="w-full max-w-xl rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-xl">
        <header className="mb-6">
          <h1 className="text-3xl font-bold tracking-tight">Vigía</h1>
          <p className="text-slate-400">
            Plataforma de monitorización de servicios y página de estado
          </p>
        </header>

        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-400">
          Conexión con la API
        </h2>

        {cargando && <p className="text-slate-400">Consultando la API…</p>}

        {error && (
          <div className="rounded-lg border border-red-900 bg-red-950/50 p-4">
            <p className="font-medium text-red-300">No se ha podido contactar con la API</p>
            <p className="mt-1 text-sm text-red-400">{error}</p>
            <p className="mt-3 text-sm text-slate-400">
              Comprueba que el backend está arrancado y que <code>VITE_API_URL</code> apunta a él.
            </p>
          </div>
        )}

        {estado && (
          <div className="rounded-lg border border-slate-800 bg-slate-950 p-4">
            <div className="mb-4 flex items-center gap-3">
              <span className="size-3 rounded-full bg-estado-activo" />
              <span className="font-medium">API operativa</span>
            </div>

            <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
              <dt className="text-slate-400">Servicio</dt>
              <dd className="font-mono">{estado.servicio}</dd>

              <dt className="text-slate-400">Versión</dt>
              <dd className="font-mono">{estado.version}</dd>

              <dt className="text-slate-400">Entorno</dt>
              <dd className="font-mono">{estado.entorno}</dd>

              <dt className="text-slate-400">Tiempo activo</dt>
              <dd className="font-mono">{estado.tiempoActivoSegundos} s</dd>

              <dt className="text-slate-400">Marca de tiempo</dt>
              <dd className="font-mono">{estado.marcaDeTiempo}</dd>
            </dl>
          </div>
        )}

        <footer className="mt-6 text-xs text-slate-500">
          Hito 1 — Boilerplate y repositorio base · Proyecto Intermodular 2º DAW
        </footer>
      </section>
    </main>
  )
}
