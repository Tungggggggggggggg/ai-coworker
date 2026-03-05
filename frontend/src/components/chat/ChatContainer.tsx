'use client';

import React from 'react';
import { useChatSimulation } from '@/hooks/useChatSimulation';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { BotMessageSquare } from 'lucide-react';

export const ChatContainer: React.FC = () => {
    const { messages, isLoading, sendMessage } = useChatSimulation();



    const handleSendMessage = (text: string) => {
        sendMessage(text, () => { });
    };

    return (
        <div className="flex flex-col h-full w-full bg-white relative overflow-hidden">
            {/* Header nhẹ nhàng cho khu vực Chat */}
            <div className="h-16 flex items-center justify-between px-6 border-b border-slate-100 bg-white shadow-sm shrink-0 z-10">
                <h2 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
                    <BotMessageSquare className="text-blue-600" size={22} />
                    Gucci Agent Simulation
                </h2>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 overflow-hidden flex flex-col relative">
                <MessageList messages={messages} isLoading={isLoading} />
            </div>

            {/* Input Area */}
            <div className="shrink-0 z-10 bg-white">
                <MessageInput onSendMessage={handleSendMessage} disabled={isLoading} />
            </div>
        </div>
    );
};
