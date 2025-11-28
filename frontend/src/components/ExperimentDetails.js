import React from 'react';

export function ExperimentDetails({ experiment, metrics, assistant, onBack }) {
  return (
    <div className="card">
      <div className="header">
        <div>
          <h2 style={{ margin: 0 }}>Experiment {experiment.id}</h2>
          <p className="small">Monitor accuracy, reward, and the best teacher assistant.</p>
        </div>
        <button className="button secondary" onClick={onBack}>Back</button>
      </div>
      <div className="metrics-grid">
        <div>
          <h4 style={{ marginTop: 0 }}>Configuration</h4>
          <p className="small">Name: {experiment.config.name}</p>
          <p className="small">Dataset: {experiment.config.dataset}</p>
          <p className="small">Teacher: {experiment.config.teacher_id}</p>
          <p className="small">Student: {experiment.config.student_id}</p>
          <p className="small">Search episodes: {experiment.config.search_episodes}</p>
          <p className="small">Status: {experiment.status}</p>
        </div>
        <div>
          <h4 style={{ marginTop: 0 }}>Student Accuracy per Episode</h4>
          {metrics.episodes.length === 0 ? (
            <p className="small">No metrics yet.</p>
          ) : (
            <ul className="small">
              {metrics.episodes.map((ep, idx) => (
                <li key={ep}>Episode {ep}: accuracy {metrics.student_accuracy[idx]}</li>
              ))}
            </ul>
          )}
        </div>
        <div>
          <h4 style={{ marginTop: 0 }}>Reward per Episode</h4>
          {metrics.episodes.length === 0 ? (
            <p className="small">No metrics yet.</p>
          ) : (
            <ul className="small">
              {metrics.episodes.map((ep, idx) => (
                <li key={ep}>Episode {ep}: reward {metrics.reward[idx]}</li>
              ))}
            </ul>
          )}
        </div>
        <div>
          <h4 style={{ marginTop: 0 }}>Best Assistant</h4>
          {assistant ? (
            <>
              <p className="small">Architecture: {assistant.architecture_id}</p>
              <p className="small">Accuracy: {assistant.val_accuracy}</p>
              <p className="small">Latency (ms): {assistant.latency_ms}</p>
              <p className="small">Params (M): {assistant.params_m}</p>
            </>
          ) : (
            <p className="small">No assistant selected yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
