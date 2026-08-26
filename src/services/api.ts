const API_BASE_URL = 'https://api.roll4rights.duckdns.org/api'

export const apiService = {
  async fetchCampaignProgress() {
    const res = await fetch(`${API_BASE_URL}/campaign-progress`)
    if (!res.ok) throw new Error(`Failed to fetch campaign progress: ${res.status}`)
    return res.json()
  },
  async fetchCampaignInfo() {
    const res = await fetch(`${API_BASE_URL}/campaign-info`)
    if (!res.ok) throw new Error(`Failed to fetch campaign info: ${res.status}`)
    return res.json()
  }
}