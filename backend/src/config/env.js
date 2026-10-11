import 'dotenv/config'

/**
 * Lee una variable de entorno y aplica un valor por defecto.
 * Si no hay valor ni defecto, se detiene el arranque: es preferible
 * fallar al iniciar que fallar a mitad de una petición.
 */
const leer = (clave, porDefecto) => {
  const valor = process.env[clave] ?? porDefecto
  if (valor === undefined) {
    throw new Error(`Falta la variable de entorno obligatoria: ${clave}`)
  }
  return valor
}

export const config = {
  entorno: leer('NODE_ENV', 'development'),
  puerto: Number(leer('PORT', '4000')),
  origenCors: leer('CORS_ORIGIN', 'http://localhost:5173'),
  version: '0.1.0'
}
