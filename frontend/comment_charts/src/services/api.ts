// src/services/api.ts
const API_URL = import.meta.env.VITE_API_URL;

export const getDashboardData = async () => {
  const [sentimentsRes, topicsRes, messagesRes] = await Promise.all([
    fetch(`${API_URL}/api/sentiments`),
    fetch(`${API_URL}/api/themes`),
    // fetch(`${API_URL}/api/messages`),
  ]);

  if (!sentimentsRes.ok || !topicsRes.ok || !messagesRes.ok) {
    throw new Error("Error API");
  }

  const sentiments = await sentimentsRes.json();
  const topics = await topicsRes.json();
  const messages = await messagesRes.json();

  return {
    sentiments,
    topics,
    messages,
  };
};