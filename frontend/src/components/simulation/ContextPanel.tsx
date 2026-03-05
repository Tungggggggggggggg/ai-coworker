'use client';

import React from 'react';
import { BookOpen, Map, Users, Info, ShieldAlert } from 'lucide-react';
import { motion } from 'framer-motion';

export const ContextPanel: React.FC = () => {
    return (
        <div className="h-full w-full bg-slate-50 border-r border-slate-200 p-6 overflow-y-auto flex flex-col gap-6 font-sans text-slate-800">

            {/* Header Profile */}
            <div className="flex flex-col gap-2">
                <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 flex items-center gap-2">
                    <BookOpen className="text-indigo-600" size={28} />
                    Gucci HQ
                </h1>
                <p className="text-sm text-slate-500 font-medium leading-relaxed">
                    Mô phỏng <strong>Lãnh Đạo Nhân Sự</strong> (HR Simulation). Bạn đang nhập vai Giám đốc Phát triển Tổ chức <strong>(OD Director)</strong>.
                </p>
            </div>

            <hr className="border-slate-200" />

            {/* Agents Map */}
            <div className="flex flex-col gap-3">
                <div className="flex items-center gap-2 text-slate-800 font-semibold">
                    <Users size={18} />
                    Hội đồng Đánh giá (Personas)
                </div>

                <div className="flex flex-col gap-2.5">
                    {/* CEO Card */}
                    <motion.div whileHover={{ scale: 1.02 }} className="bg-gradient-to-br from-indigo-900 to-indigo-800 p-4 rounded-xl shadow-md text-white border border-indigo-700">
                        <h3 className="text-sm font-bold text-yellow-500 mb-1">CEO</h3>
                        <p className="text-xs text-indigo-100 opacity-90 leading-relaxed">
                            Tập trung vào <strong>Brand Autonomy</strong>. Sẽ phản đối sự can thiệp từ tập đoàn nếu làm phai mờ DNA của 9 Maison.
                        </p>
                    </motion.div>

                    {/* CHRO Card */}
                    <motion.div whileHover={{ scale: 1.02 }} className="bg-gradient-to-br from-teal-800 to-teal-700 p-4 rounded-xl shadow-md text-white border border-teal-600">
                        <h3 className="text-sm font-bold text-teal-100 mb-1">Global CHRO</h3>
                        <p className="text-xs text-teal-50 opacity-90 leading-relaxed">
                            Trung thành với <strong>Competency Framework</strong>. Ưu tiên giải quyết luân chuyển nhân sự giữa các brand.
                        </p>
                    </motion.div>

                    {/* Regional Manager Card */}
                    <motion.div whileHover={{ scale: 1.02 }} className="bg-gradient-to-br from-emerald-700 to-emerald-600 p-4 rounded-xl shadow-md text-white border border-emerald-500">
                        <h3 className="text-sm font-bold text-emerald-100 mb-1">Regional Manager</h3>
                        <p className="text-xs text-emerald-50 opacity-90 leading-relaxed">
                            Góc nhìn Store. Nhấn mạnh <strong>Doanh Số</strong> và chỉ trích các khung nhân sự thiếu thực tế.
                        </p>
                    </motion.div>

                </div>
            </div>
        </div>
    );
};
