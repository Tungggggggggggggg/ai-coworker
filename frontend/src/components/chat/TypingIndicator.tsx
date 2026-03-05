'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Avatar } from '@/components/ui/Avatar';

export const TypingIndicator: React.FC = () => {
    return (
        <div className="flex w-full gap-4 mb-6 pt-2 pb-4">
            <Avatar role="System" className="mt-1" />
            <div className="flex bg-slate-100 px-5 py-4 rounded-2xl rounded-tl-sm w-fit items-center gap-1">
                <motion.div
                    className="w-2 h-2 bg-slate-400 rounded-full"
                    animate={{ y: [0, -5, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                />
                <motion.div
                    className="w-2 h-2 bg-slate-400 rounded-full"
                    animate={{ y: [0, -5, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                />
                <motion.div
                    className="w-2 h-2 bg-slate-400 rounded-full"
                    animate={{ y: [0, -5, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                />
            </div>
        </div>
    );
};
