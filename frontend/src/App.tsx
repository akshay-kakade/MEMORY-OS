import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useStore } from './store/useStore';
import Login from './pages/Login';
import ChatPage from './pages/ChatPage';

function App() {
  const user = useStore((state) => state.user);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
        <Route path="/" element={user ? <ChatPage /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
