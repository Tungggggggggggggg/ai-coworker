'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Avatar } from '@/components/ui/Avatar';
import { ChatMessage } from '@/types';
import { cn } from '@/lib/utils';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageBubbleProps {
    message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isUser = message.role === 'OD Director';
    const isSystem = message.role === 'System';

    if (isSystem) {
        return (
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex w-full justify-center my-4"
            >
                <span className="text-xs font-medium text-slate-500 bg-slate-100/50 px-4 py-1.5 rounded-full border border-slate-200">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                </span>
            </motion.div>
        );
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
            className={cn(
                "flex w-full gap-4 mb-6",
                isUser ? "flex-row-reverse" : "flex-row"
            )}
        >
            <Avatar role={message.role} className="mt-1" />

            <div className={cn(
                "flex max-w-[80%] flex-col",
                isUser ? "items-end" : "items-start"
            )}>
                <span className="text-xs text-slate-400 mb-1 ml-1 mr-1">{message.role}</span>
                <div className={cn(
                    "relative px-5 py-3.5 text-sm shadow-sm",
                    isUser
                        ? "bg-blue-600 text-white rounded-2xl rounded-tr-sm"
                        : "bg-white text-slate-800 border border-slate-100 rounded-2xl rounded-tl-sm drop-shadow-sm prose prose-sm prose-slate max-w-none"
                )}>
                    {isUser ? (
                        <div className="whitespace-pre-wrap leading-relaxed">
                            {message.content}
                        </div>
                    ) : (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {message.content}
                        </ReactMarkdown>
                    )}
                </div>
            </div>
        </motion.div>
    );
};
