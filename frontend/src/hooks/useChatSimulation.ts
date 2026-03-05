import { useState, useCallback, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { ChatMessage, ChatResponsePayload } from '@/types';
import { chatApi } from '@/lib/api';

export function useChatSimulation() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    // Lưu state Session ID (Nếu app refresh thì tạo mới session, hoặc có thể dùng localStorage)
    const sessionIdRef = useRef<string>('');

    useEffect(() => {
        // Component Mount -> Tạo phiền chat ID unique
        sessionIdRef.current = `sess-${uuidv4()}`;

        // Welcome message đầu tiên từ Hệ thống
        setMessages([
            {
                role: 'System',
                content: 'Chào mừng bạn đến với Gucci AI Co-Worker Engine. OD Director (Bạn) hãy bắt đầu đề xuất ý tưởng nhân sự cho Tập đoàn!'
            }
        ]);
    }, []);

    const sendMessage = useCallback(async (text: string, onMetricsUpdate: (lat: number, tok: number) => void) => {
        if (!text.trim() || isLoading) return;

        setIsLoading(true);
        // 1. Thêm tin nhắn của User ngay lập tức vào UI
        const userMsg: ChatMessage = { role: 'OD Director', content: text };
        setMessages(prev => [...prev, userMsg]);

        try {
            // 2. Gửi request sang FastAPI Backend
            const response: ChatResponsePayload = await chatApi.sendMessage({
                session_id: sessionIdRef.current,
                message: text
            });

            // 3. Update Metrics callback (để OpsBadge Component update UI nhỏ)
            onMetricsUpdate(response.latency_ms, response.estimated_tokens);

            // 4. Update Chat box
            const aiMsg: ChatMessage = {
                role: response.agent_name,
                content: response.reply
            };
            setMessages(prev => [...prev, aiMsg]);

        } catch (error) {
            console.error("Chat API error:", error);
            setMessages(prev => [...prev, {
                role: 'System',
                content: 'Lỗi Call sang LangGraph API. Vui lòng kiểm tra console Backend.'
            }]);
        } finally {
            setIsLoading(false);
        }
    }, [isLoading]);

    return { messages, isLoading, sendMessage };
}
