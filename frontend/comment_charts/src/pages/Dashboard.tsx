import { useEffect, useState } from "react";
import type { DashboardData } from "../type";
import { getDashboardData } from "../services/api";

import SentimentChart from "../components/SentimentChart";
import TopicsChart from "../components/TopicsChart";
import MessagesFeed from "../components/MessagesFeed";

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const load = async () => {
    try {
      const result = await getDashboardData();
      console.log("🚀 ~ load ~ result:", result)
      setData(result);
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    load();
  }, []);

  if (!data) return <p className="p-6">Cargando...</p>;

  return (
    <div className="p-6 space-y-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold">Dashboard de Sentimientos</h1>

      <div className="grid md:grid-cols-2 gap-6">
        <SentimentChart data={data.sentiments} />
        <TopicsChart data={data.topics} />
      </div>

      <MessagesFeed messages={data.messages} />
    </div>
  );
}