// src/types/index.ts
export interface Sentiment {
  name: string;
  value: number;
}

export interface Topic {
  name: string;
  value: number;
}

export interface Message {
  id: number;
  texto_mensaje: string;
  sentimiento: string;
  tema: string;
}

export interface DashboardData {
  sentiments: Sentiment[];
  topics: Topic[];
  messages: Message[];
}