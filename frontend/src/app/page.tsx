import AgentDashboard from '../components/AgentDashboard';

export default function Home() {
  return (
    <main className="min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">Agent Management System</h1>
      <AgentDashboard />
    </main>
  );
}