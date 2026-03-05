'use client';

import React from 'react';
import { Gauge, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';

interface OpsBadgeProps {
    latency_ms: number;
    estimated_tokens: number;
    className?: string;
}

export const OpsBadge: React.FC<OpsBadgeProps> = ({ latency_ms, estimated_tokens, className }) => {
    return (
        <div className={cn(
            "flex items-center gap-3 px-3 py-1 bg-slate-50/50 rounded-full border border-slate-100/50 text-[10px] font-medium text-slate-400 select-none transition-all hover:bg-slate-100/50 hover:border-slate-200",
            className
        )}>
            <div className="flex items-center gap-1">
                <Gauge size={10} className="text-blue-500/70" />
                <span className="tabular-nums">{latency_ms.toFixed(0)}ms</span>
            </div>

            <div className="w-[1px] h-2 bg-slate-200" />

            <div className="flex items-center gap-1">
                <Zap size={10} className="text-amber-500/70" />
                <span className="tabular-nums">{estimated_tokens} tokens</span>
            </div>
        </div>
    );
};
