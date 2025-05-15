import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const FluentAI_DRLGUIDashboard = () => {
  const [trainingProgress, setTrainingProgress] = useState(0);
  const [episodeData, setEpisodeData] = useState([
    { episode: 1, reward: 0 },
    { episode: 2, reward: 0 },
    { episode: 3, reward: 0 },
  ]);

  const startTraining = () => {
    setTrainingProgress(0);
    const interval = setInterval(() => {
      setTrainingProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 5;
      });

      setEpisodeData((prevData) => [
        ...prevData,
        { episode: prevData.length + 1, reward: Math.random() * 100 },
      ]);
    }, 500);
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">FluentAI Deep Reinforcement Learning Dashboard</h1>
      <Card className="mb-4">
        <CardContent>
          <h2 className="text-lg font-semibold">Training Progress</h2>
          <Progress value={trainingProgress} className="mt-2" />
          <Button className="mt-4" onClick={startTraining} disabled={trainingProgress >= 100}>
            {trainingProgress >= 100 ? "Training Completed" : "Start Training"}
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-lg font-semibold">Training Performance</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={episodeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="episode" label={{ value: "Episode", position: "insideBottomRight", offset: -5 }} />
              <YAxis label={{ value: "Reward", angle: -90, position: "insideLeft" }} />
              <Tooltip />
              <Line type="monotone" dataKey="reward" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};

export default FluentAI_DRLGUIDashboard;
