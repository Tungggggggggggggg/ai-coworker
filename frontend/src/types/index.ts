export interface ChatMessage {
    role: "OD Director" | "Supervisor" | "CEO" | "CHRO" | "Manager" | "System" | string;
    content: string;
    latency_ms?: number;
    estimated_tokens?: number;
}

export interface ChatRequestPayload {
    session_id: string;
    message: string;
}

export interface ChatResponsePayload {
    agent_name: string;
    reply: string;
    latency_ms: number;
    estimated_tokens: number;
}

export interface MetricsPayload {
    total_latency_ms: number;
    total_tokens: number;
}
