import { useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import KnowledgeBase from '../components/KnowledgeBase';
import KnowledgeGraph from '../components/KnowledgeGraph';
import { useStore } from '../store/useStore';
import api from '../api/axios';

const ChatPage = () => {
  const { user, setWorkspaces, setCurrentWorkspace, setChats, view } = useStore();

  useEffect(() => {
    const fetchInitialData = async () => {
      if (!user) return;
      try {
        const wsRes = await api.get('/workspaces/', { params: { user_id: user.id } });
        setWorkspaces(wsRes.data);
        if (wsRes.data.length > 0) {
          setCurrentWorkspace(wsRes.data[0]);
          const chatRes = await api.get('/chats/', { params: { workspace_id: wsRes.data[0].id } });
          setChats(chatRes.data);
        } else {
          // Create default workspace if none exists
          const newWsRes = await api.post('/workspaces/', {
            name: 'General',
            description: 'My first workspace',
            owner_id: user.id
          });
          setWorkspaces([newWsRes.data]);
          setCurrentWorkspace(newWsRes.data);
        }
      } catch (err) {
        console.error('Failed to fetch initial data', err);
      }
    };

    fetchInitialData();
  }, [user, setWorkspaces, setCurrentWorkspace, setChats]);

  const renderView = () => {
    switch (view) {
      case 'chat': return <ChatWindow />;
      case 'knowledge': return <KnowledgeBase />;
      case 'graph': return <KnowledgeGraph />;
      default: return <ChatWindow />;
    }
  };

  return (
    <div className="relative flex h-screen overflow-hidden font-sans app-aurora-bg">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 relative z-10">
        {renderView()}
      </main>
    </div>
  );
};

export default ChatPage;
