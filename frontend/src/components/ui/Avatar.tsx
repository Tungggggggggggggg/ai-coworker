import React from 'react';
import { UserCircle, ShieldAlert, BadgeInfo, BriefcaseBusiness, Store } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AvatarProps {
    role: string | null;
    className?: string;
}

export const Avatar: React.FC<AvatarProps> = ({ role, className }) => {
    // Config màu sắc và icon tuỳ theo người nói
    const agentConfigs: Record<string, { bg: string, text: string, icon: React.ReactNode }> = {
        'OD Director': { bg: 'bg-blue-100', text: 'text-blue-800', icon: <UserCircle size={20} /> },
        'CEO': { bg: 'bg-indigo-900', text: 'text-yellow-400', icon: <BriefcaseBusiness size={20} /> },
        'CHRO': { bg: 'bg-teal-700', text: 'text-white', icon: <BadgeInfo size={20} /> },
        'Manager': { bg: 'bg-emerald-600', text: 'text-white', icon: <Store size={20} /> },
        'Supervisor': { bg: 'bg-rose-600', text: 'text-white', icon: <ShieldAlert size={20} /> },
        'System': { bg: 'bg-gray-200', text: 'text-gray-600', icon: <BadgeInfo size={20} /> },
    };

    const nameMap: Record<string, string> = {
        'OD Director': 'You',
        'CEO': 'CEO (Gucci)',
        'CHRO': 'Global CHRO',
        'Manager': 'Regional Mgr',
        'Supervisor': 'AI Guard',
        'System': 'System',
    };

    // Mặc định cho Hệ thống nếu role undefined
    // Normalize role string to handle mixed case ("supervisor" vs "Supervisor")
    const normalizedRole = role ? (role.toLowerCase() === 'supervisor' ? 'Supervisor' : role) : 'System';

    const config = agentConfigs[normalizedRole] || agentConfigs['System'];
    const displayName = nameMap[normalizedRole] || normalizedRole;

    return (
        <div className={cn("flex flex-col items-center gap-1", className)}>
            <div className={cn(
                "flex h-10 w-10 shrink-0 items-center justify-center rounded-full shadow-sm drop-shadow-md",
                config.bg, config.text
            )}>
                {config.icon}
            </div>
            <span className="text-[10px] font-semibold text-gray-500 max-w-[60px] text-center leading-tight truncate">
                {displayName}
            </span>
        </div>
    );
};
