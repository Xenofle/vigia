import express from 'express'
import cors from 'cors'

import { config } from './config/env.js'
import { healthRouter } from './routes/health.routes.js'
import { noEncontrado, manejadorErrores } from './middlewares/errores.js'

/**
 * Construye la aplicación Express sin arrancarla.
 * Separar la construcción del arranque permite montar la misma app
 * en las pruebas automáticas sin ocupar un puerto.
 */
export const crearApp = () => {
  const app = express()

  app.use(cors({ origin: config.origenCors }))
  app.use(express.json())

  app.use('/api', healthRouter)

  app.use(noEncontrado)
  app.use(manejadorErrores)

  return app
}
