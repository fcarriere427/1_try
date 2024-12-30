import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Table } from "lucide-react";

const AgentDashboard = () => {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [agents, setAgents] = useState([]);

  // Simulation de données pour l'exemple
  useEffect(() => {
    // Dans une vraie application, ces données viendraient de votre backend Python
    const mockAgents = [
      {
        name: "Agent_1",
        dna: {
          web_search_ability: 0.8,
          synthesis_ability: 0.6,
          web_action_ability: 0.7,
          creativity: 0.9,
          focus: 0.75
        },
        fitness: 0.82,
        actions_history: [
          { timestamp: "2024-01-01", success: true, task: "web_search" },
          { timestamp: "2024-01-02", success: false, task: "synthesis" }
        ]
      }
      // ... autres agents
    ];
    setAgents(mockAgents);
  }, []);

  const DNAVisualization = ({ dna }) => {
    const dnaData = Object.entries(dna).map(([key, value]) => ({
      trait: key,
      value: value * 100
    }));

    return (
      <Card className="w-full mb-4">
        <CardHeader>
          <CardTitle>DNA Profile</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dnaData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="trait" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="p-4 space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Liste des agents */}
        <Card>
          <CardHeader>
            <CardTitle>Agents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {agents.map(agent => (
                <div
                  key={agent.name}
                  className="p-2 border rounded cursor-pointer hover:bg-gray-100"
                  onClick={() => setSelectedAgent(agent)}
                >
                  <div className="font-medium">{agent.name}</div>
                  <div className="text-sm text-gray-600">Fitness: {agent.fitness}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Détails de l'agent sélectionné */}
        {selectedAgent && (
          <Card>
            <CardHeader>
              <CardTitle>{selectedAgent.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <DNAVisualization dna={selectedAgent.dna} />
              
              <div className="mt-4">
                <h3 className="font-medium mb-2">Action History</h3>
                <div className="space-y-1">
                  {selectedAgent.actions_history.map((action, idx) => (
                    <div key={idx} className="text-sm">
                      <span className={action.success ? "text-green-600" : "text-red-600"}>
                        {action.success ? "✓" : "✗"}
                      </span>
                      {" "}
                      {action.task} - {action.timestamp}
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default AgentDashboard;