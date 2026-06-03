import { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';
import api from '../api/axios';
import { Network, RefreshCw, ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';

const KnowledgeGraph = () => {
  const { currentWorkspace } = useStore();
  const [graphImage, setGraphImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchGraph = async () => {
    if (!currentWorkspace) return;
    setLoading(true);
    try {
      const res = await api.get(`/graph/${currentWorkspace.id}`);
      setGraphImage(res.data.image);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchGraph();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentWorkspace]);

  return (
    <div className="flex-1 flex flex-col min-w-0 bg-background overflow-hidden">
      <header className="h-16 border-b border-border flex items-center justify-between px-6 bg-background/80 backdrop-blur-md sticky top-0 z-10">
        <h1 className="text-xl font-bold">Knowledge Graph</h1>
        <div className="flex items-center gap-2">
          <button 
            onClick={fetchGraph}
            disabled={loading}
            className="p-2 hover:bg-panel-lighter rounded-lg text-muted transition-colors disabled:opacity-50"
          >
            <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
          </button>
        </div>
      </header>

      <div className="flex-1 p-8 flex items-center justify-center bg-[#0a0c10]">
        <div className="relative w-full max-w-5xl aspect-video bg-panel border border-border rounded-3xl overflow-hidden shadow-2xl group">
          {graphImage ? (
            <img 
              src={`data:image/png;base64,${graphImage}`} 
              alt="Knowledge Graph" 
              className="w-full h-full object-contain"
            />
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center text-muted space-y-4">
              <div className="w-16 h-16 bg-panel-lighter rounded-2xl flex items-center justify-center">
                <Network size={32} />
              </div>
              <p>No graph data available for this workspace.</p>
              <button 
                onClick={fetchGraph}
                className="px-4 py-2 bg-accent text-background font-bold rounded-xl hover:bg-accent/90 transition-all"
              >
                Generate Graph
              </button>
            </div>
          )}
          
          <div className="absolute bottom-6 right-6 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button className="p-3 bg-panel-lighter/80 backdrop-blur border border-border rounded-xl hover:bg-panel-lighter transition-all shadow-lg"><ZoomIn size={20} /></button>
            <button className="p-3 bg-panel-lighter/80 backdrop-blur border border-border rounded-xl hover:bg-panel-lighter transition-all shadow-lg"><ZoomOut size={20} /></button>
            <button className="p-3 bg-panel-lighter/80 backdrop-blur border border-border rounded-xl hover:bg-panel-lighter transition-all shadow-lg"><Maximize2 size={20} /></button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeGraph;
