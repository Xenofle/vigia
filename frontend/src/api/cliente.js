const URL_API = import.meta.env.VITE_API_URL ?? 'http://localhost:4000/api'

/**
 * Cliente mínimo de la API.
 * Centraliza la URL base para no repetirla por los componentes.
 */
export const consultarApi = async (ruta) => {
  const respuesta = await fetch(`${URL_API}${ruta}`)

  if (!respuesta.ok) {
    throw new Error(`La API respondió con el código ${respuesta.status}`)
  }

  return respuesta.json()
}

export const obtenerEstadoApi = () => consultarApi('/health')
