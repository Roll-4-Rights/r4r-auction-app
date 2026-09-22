const BASE_URL = import.meta.env.VITE_API_URL

export async function apiFetch(path: string, options: RequestInit = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    credentials: 'include', // required so the bidder's login cookie is sent/received
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  return response
}