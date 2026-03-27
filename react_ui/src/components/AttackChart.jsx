import { LineChart, Line, XAxis, YAxis } from "recharts";

function AttackChart({ data }) {
  const chartData = data.map((d, i) => ({
    index: i,
    severity:
      d.severity === "NORMAL" ? 0 :
      d.severity === "MEDIUM" ? 1 :
      d.severity === "HIGH" ? 2 : 3
  }));

  return (
    <LineChart width={700} height={250} data={chartData}>
      <XAxis dataKey="index" />
      <YAxis />
      <Line dataKey="severity" />
    </LineChart>
  );
}

export default AttackChart;
