const API_BASE_URL = `${import.meta.env.VITE_API_URL}/api`

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
  },
  // Paginated: pass `limit` (page size) and `offset`. Returns NocoDB's
  // raw envelope { list, pageInfo } — pageInfo.totalRows / isLastPage
  // drive the Next/Previous controls on the donator-info page.
  async fetchDonatorProfiles(params: { limit?: number; offset?: number } = {}) {
    const query = new URLSearchParams()
    if (params.limit !== undefined) query.set('limit', String(params.limit))
    if (params.offset !== undefined) query.set('offset', String(params.offset))
    const qs = query.toString()
    const res = await fetch(`${API_BASE_URL}/donator-profiles${qs ? `?${qs}` : ''}`)
    if (!res.ok) throw new Error(`Failed to fetch donator profiles: ${res.status}`)
    return res.json()
  }
}