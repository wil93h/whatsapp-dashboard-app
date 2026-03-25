export default function MessagesFeed({ messages }: any) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="mb-4 font-bold">Mensajes Recientes</h2>

      <div className="space-y-3 max-h-[400px] overflow-y-auto">
        {messages.map((m: any) => (
          <div key={m.id} className="border rounded p-3">
            <p className="font-semibold">{m.texto_mensaje}</p>

            <div className="text-sm text-gray-500 flex gap-2 mt-1">
              <span>Sentimiento:</span>
              <span className="font-medium">{m.sentimiento}</span>
              <span>|</span>
              <span>Tema:</span>
              <span className="font-medium">{m.tema}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}