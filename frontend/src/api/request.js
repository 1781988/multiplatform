const BASE_URL = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export async function apiRequest(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(options.headers || {})
    },
    ...options
  });

  let data = null;
  try {
    data = await response.json();
  } catch (error) {
    data = { code: response.status, message: "" };
  }

  if (!response.ok && data && typeof data.code === "undefined") {
    return { code: response.status, message: response.statusText, data: null };
  }

  return data;
}
