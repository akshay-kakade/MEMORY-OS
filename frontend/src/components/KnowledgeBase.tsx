import { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';
import api from '../api/axios';
import { Search, Trash2, Pin, Calendar, Star } from 'lucide-react';
import { motion } from 'framer-motion';

const KnowledgeBase = () => {
  const { currentWorkspace } = useStore();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [memories, setMemories] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchMemories = async () => {
      if (!currentWorkspace) return;
      setLoading(true);
      try {
        const res = await api.get(`/memories/${currentWorkspace.id}`);
        setMemories(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchMemories();
  }, [currentWorkspace]);

  const filteredMemories = memories.filter(m => 
    m.content.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex-1 flex flex-col min-w-0 bg-background overflow-hidden">
      <header className="h-16 border-b border-border flex items-center justify-between px-6 bg-background/80 backdrop-blur-md sticky top-0 z-10">
        <h1 className="text-xl font-bold">Knowledge Base</h1>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" size={16} />
          <input 
            type="text" 
            placeholder="Search memories..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 pr-4 py-2 bg-panel border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent transition-all text-sm w-64"
          />
        </div>
      </header>

      <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredMemories.map((memory, i) => (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                key={memory.id}
                className="bg-panel border border-border rounded-2xl p-5 hover:border-accent/30 transition-all group relative overflow-hidden"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="px-2 py-1 bg-accent/10 text-accent text-[10px] font-bold uppercase tracking-wider rounded-md border border-accent/20">
                    {memory.category_id === 1 ? 'Preference' : 'Fact'}
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="text-muted hover:text-accent transition-colors"><Pin size={14} /></button>
                    <button className="text-muted hover:text-red-500 transition-colors"><Trash2 size={14} /></button>
                  </div>
                </div>
                <p className="text-sm leading-relaxed mb-6 line-clamp-4 group-hover:line-clamp-none transition-all">
                  {memory.content}
                </p>
                <div className="mt-auto pt-4 border-t border-border/50 flex items-center justify-between text-[10px] text-muted font-medium">
                  <div className="flex items-center gap-1.5">
                    <Calendar size={12} />
                    {new Date(memory.created_at).toLocaleDateString()}
                  </div>
                  <div className="flex items-center gap-1">
                    <Star size={12} className="text-accent" />
                    Importance: {memory.importance}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
          
          {!loading && filteredMemories.length === 0 && (
            <div className="text-center py-20">
              <div className="w-20 h-20 bg-panel border border-border rounded-3xl flex items-center justify-center mx-auto mb-6 text-muted">
                <Search size={32} />
              </div>
              <h3 className="text-lg font-bold mb-2">No memories found</h3>
              <p className="text-muted">Try a different search or chat more to build your knowledge base.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default KnowledgeBase;
