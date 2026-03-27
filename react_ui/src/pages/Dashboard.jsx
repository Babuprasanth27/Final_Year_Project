import { useEffect, useState } from "react";
import { liveDetect } from "../services/api";
import StatCard from "../components/StatCard";
import AttackChart from "../components/AttackChart";
import AttackTable from "../components/AttackTable";

function Dashboard() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const timer = setInterval(async () => {
      const res = await liveDetect();
      setLogs(prev => [res.data, ...prev.slice(0, 20)]);
    }, 3000);

    return () => clearInterval(timer);
  }, []);

  return (
    <>
      <div className="stats">
        <StatCard title="Total Records" value={logs.length} />
        <StatCard
          title="Critical Attacks"
          value={logs.filter(l => l.severity === "CRITICAL").length}
        />
      </div>

      <AttackChart data={logs} />
      <AttackTable data={logs} />
    </>
  );
}

export default Dashboard;
