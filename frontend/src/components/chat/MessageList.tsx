'use client';

import React, { useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';
import { ChatMessage } from '@/types';
import { AnimatePresence } from 'framer-motion';

interface MessageListProps {
    messages: ChatMessage[];
    isLoading: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        // Auto scroll bottom khi có tin nhắn mới hoặc loading state
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    return (
        <div className="flex-1 overflow-y-auto w-full p-4 md:p-6 lg:p-8 space-y-2 scroll-smooth bg-slate-50/50">
            <AnimatePresence>
                {messages.map((msg, idx) => (
                    <MessageBubble key={idx} message={msg} />
                ))}
                {isLoading && <TypingIndicator key="typing-indicator" />}
            </AnimatePresence>
            <div ref={bottomRef} className="h-6 w-full" />
        </div>
    );
};
