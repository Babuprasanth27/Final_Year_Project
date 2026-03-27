function AttackTable({ data }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Source IP</th>
          <th>Prediction</th>
          <th>Severity</th>
        </tr>
      </thead>
      <tbody>
        {data.map((d, i) => (
          <tr key={i}>
            <td>{d.src_ip}</td>
            <td>{d.prediction}</td>
            <td className={d.severity}>{d.severity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default AttackTable;
