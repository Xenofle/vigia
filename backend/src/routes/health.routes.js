import { Router } from 'express'
import { config } from '../config/env.js'

export const healthRouter = Router()

/**
 * GET /api/health
 * Endpoint de comprobación del Hito 1: confirma que la API está viva
 * y permite al frontend demostrar la comunicación entre ambas partes.
 */
healthRouter.get('/health', (req, res) => {
  res.json({
    estado: 'ok',
    servicio: 'vigia-api',
    version: config.version,
    entorno: config.entorno,
    marcaDeTiempo: new Date().toISOString(),
    tiempoActivoSegundos: Math.round(process.uptime())
  })
})
