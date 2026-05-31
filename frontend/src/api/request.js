const BASE_URL = (import.meta.env.VITE_API_BASE || "").replace(/\/$/, "");

export async function apiRequest(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const timeout = options.timeout ?? 30000;
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), timeout);
  let response;
  try {
    const url = path.startsWith("http") ? path : `${BASE_URL}${path}`;
    response = await fetch(url, {
      headers: {
        ...(isFormData ? {} : { "Content-Type": "application/json" }),
        ...(options.headers || {})
      },
      ...options,
      signal: options.signal || controller.signal
    });
  } catch (error) {
    const isTimeout = error?.name === "AbortError";
    return {
      code: isTimeout ? 408 : 0,
      message: isTimeout ? "请求超时，请稍后重试" : "无法连接后端服务，请确认 FastAPI 服务已启动",
      data: null
    };
  } finally {
    window.clearTimeout(timer);
  }

  let data = null;
  try {
    data = await response.json();
  } catch (error) {
    data = { code: response.status, message: response.statusText || "请求失败", data: null };
  }

  if (!response.ok) {
    if (data && typeof data.code !== "undefined") return data;
    return { code: response.status, message: response.statusText, data: null };
  }

  return data;
}
