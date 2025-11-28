import React, { useEffect, useState } from 'react';
import { Api } from './api';
import { Dashboard } from './components/Dashboard';
import { ExperimentForm } from './components/ExperimentForm';
import { ExperimentDetails } from './components/ExperimentDetails';

function useExperiments() {
  const [experiments, setExperiments] = useState([]);
  const refresh = () => Api.listExperiments().then(setExperiments);
  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 2000);
    return () => clearInterval(interval);
  }, []);
  return { experiments, refresh };
}

function useModelOptions() {
  const [teachers, setTeachers] = useState([]);
  const [students, setStudents] = useState([]);
  useEffect(() => {
    Api.listTeachers().then(setTeachers);
    Api.listStudents().then(setStudents);
  }, []);
  return { teachers, students };
}

export default function App() {
  const { experiments, refresh } = useExperiments();
  const { teachers, students } = useModelOptions();
  const [mode, setMode] = useState('dashboard');
  const [selectedId, setSelectedId] = useState(null);
  const [detail, setDetail] = useState(null);
  const [metrics, setMetrics] = useState({ episodes: [], student_accuracy: [], reward: [] });
  const [assistant, setAssistant] = useState(null);

  useEffect(() => {
    if (selectedId) {
      Api.getExperiment(selectedId).then(setDetail);
      Api.getMetrics(selectedId).then(setMetrics);
      Api.getBestAssistant(selectedId).then(setAssistant).catch(() => setAssistant(null));
    }
  }, [selectedId]);

  const handleSubmit = async (payload) => {
    await Api.createExperiment(payload);
    refresh();
    setMode('dashboard');
  };

  const openDetails = (id) => {
    setSelectedId(id);
    setMode('details');
  };

  const goHome = () => {
    setMode('dashboard');
    setSelectedId(null);
    setDetail(null);
    setAssistant(null);
    setMetrics({ episodes: [], student_accuracy: [], reward: [] });
  };

  return (
    <div className="app-shell">
      <div className="header">
        <div>
          <p className="small" style={{ marginBottom: 4 }}>A3KD – Adaptive Assistant Architecture Search</p>
          <h1 style={{ margin: 0 }}>Knowledge Distillation Playground</h1>
        </div>
        <div className="small">Backend URL: {process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}</div>
      </div>

      {mode === 'dashboard' && (
        <>
          <Dashboard experiments={experiments} onCreateClick={() => setMode('create')} onSelect={openDetails} />
          <div className="card">
            <p className="small">Create new A3KD runs, monitor student accuracy, and compare TA architectures.</p>
          </div>
        </>
      )}

      {mode === 'create' && (
        <ExperimentForm
          teachers={teachers}
          students={students}
          onSubmit={handleSubmit}
          onCancel={() => setMode('dashboard')}
        />
      )}

      {mode === 'details' && detail && (
        <ExperimentDetails
          experiment={detail}
          metrics={metrics}
          assistant={assistant}
          onBack={goHome}
        />
      )}
    </div>
  );
}
