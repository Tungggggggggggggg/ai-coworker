import { ChatContainer } from '@/components/chat/ChatContainer';
import { ContextPanel } from '@/components/simulation/ContextPanel';

export default function Home() {
  return (
    <main className="flex h-screen w-full overflow-hidden bg-slate-100">

      {/* Vùng Trữ Context (1/3 Màn Hình Trái) - Ẩn trên Mobile */}
      <section className="hidden md:flex flex-col w-[380px] shrink-0 border-r border-slate-200">
        <ContextPanel />
      </section>

      {/* Vùng Trò Chuyện Lõi (Phần Lớn Màn Hình) */}
      <section className="flex-1 flex flex-col min-w-0 bg-white shadow-xl shadow-slate-200/50 z-10 relative">
        <ChatContainer />
      </section>

    </main>
  );
}
