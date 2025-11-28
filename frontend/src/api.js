const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

async function http(method, path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  return res.json();
}

export const Api = {
  health: () => http('GET', '/health'),
  listTeachers: () => http('GET', '/models/teachers'),
  listStudents: () => http('GET', '/models/students'),
  listExperiments: () => http('GET', '/experiments'),
  createExperiment: (payload) => http('POST', '/experiments', payload),
  getExperiment: (id) => http('GET', `/experiments/${id}`),
  getMetrics: (id) => http('GET', `/experiments/${id}/metrics`),
  getBestAssistant: (id) => http('GET', `/experiments/${id}/best-assistant`),
};
