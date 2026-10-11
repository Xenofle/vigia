/** Captura cualquier ruta no definida y responde en JSON, no en HTML. */
export const noEncontrado = (req, res) => {
  res.status(404).json({
    error: 'Recurso no encontrado',
    ruta: req.originalUrl
  })
}

/** Manejador de errores centralizado. Express 5 lo identifica por sus 4 parámetros. */
// eslint-disable-next-line no-unused-vars
export const manejadorErrores = (err, req, res, next) => {
  console.error('[vigia-api] error no controlado:', err)
  res.status(err.status ?? 500).json({
    error: err.message ?? 'Error interno del servidor'
  })
}
