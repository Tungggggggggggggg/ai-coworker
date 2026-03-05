'use client';

import React, { useState, KeyboardEvent } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface MessageInputProps {
    onSendMessage: (text: string) => void;
    disabled: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, disabled }) => {
    const [text, setText] = useState('');

    const handleSend = () => {
        if (text.trim() && !disabled) {
            onSendMessage(text);
            setText('');
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="relative p-4 bg-white/50 backdrop-blur-sm border-t border-slate-200">
            <div className="relative flex items-end gap-2 bg-white rounded-2xl border border-slate-200 shadow-sm focus-within:border-blue-400 focus-within:ring-4 focus-within:ring-blue-400/10 transition-all duration-200 p-2">
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={disabled}
                    placeholder="Đề xuất kiến trúc nhân sự One HR của bạn tới CEO/CHRO..."
                    className="w-full max-h-32 min-h-[44px] bg-transparent resize-none outline-none py-3 px-3 text-sm text-slate-700 placeholder:text-slate-400 disabled:opacity-50"
                    rows={1}
                />

                <AnimatePresence>
                    {text.trim() && !disabled && (
                        <motion.button
                            initial={{ scale: 0, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0, opacity: 0 }}
                            transition={{ type: "spring", stiffness: 400, damping: 20 }}
                            onClick={handleSend}
                            className="p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-md transition-colors flex shrink-0"
                        >
                            <Send size={18} />
                        </motion.button>
                    )}
                </AnimatePresence>
            </div>

            <div className="text-center mt-3 flex justify-center items-center gap-1.5 text-xs text-slate-400">
                <Sparkles size={12} className="text-amber-500" />
                Bảo mật LLM: Supervisor AI sẽ chặn các lệnh Jailbreak.
            </div>
        </div>
    );
};
