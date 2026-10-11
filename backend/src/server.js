import { crearApp } from './app.js'
import { config } from './config/env.js'

const app = crearApp()

app.listen(config.puerto, () => {
  console.log(
    `[vigia-api] escuchando en http://localhost:${config.puerto}/api/health (entorno: ${config.entorno})`
  )
})
