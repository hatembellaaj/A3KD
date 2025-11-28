import React from 'react';

export function Dashboard({ experiments, onCreateClick, onSelect }) {
  return (
    <div className="card">
      <div className="header">
        <div>
          <h2 style={{ margin: 0 }}>Experiments</h2>
          <p className="small">Track all A3KD searches in one place.</p>
        </div>
        <button className="button" onClick={onCreateClick}>New Experiment</button>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Dataset</th>
            <th>Teacher</th>
            <th>Student</th>
            <th>Status</th>
            <th>Best Accuracy</th>
          </tr>
        </thead>
        <tbody>
          {experiments.map((exp) => (
            <tr key={exp.id} style={{ cursor: 'pointer' }} onClick={() => onSelect(exp.id)}>
              <td className="mono">{exp.id}</td>
              <td>{exp.name}</td>
              <td>{exp.dataset}</td>
              <td>{exp.teacher_id}</td>
              <td>{exp.student_id}</td>
              <td>{exp.status}</td>
              <td>{exp.best_accuracy?.toFixed(3)}</td>
            </tr>
          ))}
          {experiments.length === 0 && (
            <tr>
              <td colSpan={7} className="small">No experiments yet.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
