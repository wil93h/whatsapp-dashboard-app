import { PieChart, Pie, Tooltip, Cell, Legend } from "recharts";

const COLORS = ["#22c55e", "#ef4444", "#eab308"]; 
// verde = positivo, rojo = negativo, amarillo = neutro

export default function SentimentChart({ data }: any) {
  return (
    <div className="bg-white p-4 rounded shadow flex flex-col items-center">
      <h2 className="mb-4 font-bold">Sentimientos</h2>

      <PieChart width={350} height={300}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          outerRadius={100}
          label
        >
          {data.map((_: any, i: number) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>

        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}