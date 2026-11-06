const API_URL = import.meta.env.VITE_API_URL
/**
* Llama a GET /api/hello y devuelve el mensaje.
* @param {string} name Nombre opcional
* @returns {Promise<string>} "Hello World" o "Hello World <name>"
*/
export async function getHello(name = '') {
const url = new URL(`${API_URL}/hello`)
const cleanName = name.trim()
if (cleanName !== '') {
// searchParams codifica correctamente espacios, tildes, etc.
url.searchParams.set('name', cleanName)
}
const response = await fetch(url, {
headers: { Accept: 'application/json' },
})
if (!response.ok) {
throw new Error(`Error ${response.status} al llamar a la API`)
}
const data = await response.json()
return data.message
}