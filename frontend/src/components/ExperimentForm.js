import React, { useMemo, useState } from 'react';

const datasets = ['CIFAR-100', 'CIFAR-10'];

export function ExperimentForm({ teachers, students, onSubmit, onCancel }) {
  const [form, setForm] = useState({
    name: '',
    dataset: datasets[0],
    teacher_id: teachers[0]?.id || '',
    student_id: students[0]?.id || '',
    search_episodes: 10,
  });

  const canSubmit = useMemo(() =>
    form.name && form.teacher_id && form.student_id && form.search_episodes > 0,
  [form]);

  const update = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const handleSubmit = (e) => {
    e.preventDefault();
    if (canSubmit) {
      onSubmit({
        ...form,
        search_episodes: Number(form.search_episodes),
      });
    }
  };

  return (
    <div className="card">
      <div className="header">
        <div>
          <h2 style={{ margin: 0 }}>New Experiment</h2>
          <p className="small">Configure the A3KD search and launch it.</p>
        </div>
        <button className="button secondary" onClick={onCancel}>Back</button>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <label className="label">
            Experiment name
            <input className="input" value={form.name} onChange={(e) => update('name', e.target.value)} required />
          </label>
          <label className="label">
            Dataset
            <select className="select" value={form.dataset} onChange={(e) => update('dataset', e.target.value)}>
              {datasets.map((ds) => <option key={ds} value={ds}>{ds}</option>)}
            </select>
          </label>
          <label className="label">
            Teacher model
            <select className="select" value={form.teacher_id} onChange={(e) => update('teacher_id', e.target.value)}>
              {teachers.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
          </label>
          <label className="label">
            Student model
            <select className="select" value={form.student_id} onChange={(e) => update('student_id', e.target.value)}>
              {students.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
          </label>
          <label className="label">
            Search episodes
            <input className="input" type="number" min="1" max="200" value={form.search_episodes}
              onChange={(e) => update('search_episodes', e.target.value)} />
          </label>
        </div>
        <div style={{ marginTop: 16, display: 'flex', justifyContent: 'flex-end', gap: 12 }}>
          <button className="button secondary" type="button" onClick={onCancel}>Cancel</button>
          <button className="button" type="submit" disabled={!canSubmit}>Create & Start</button>
        </div>
      </form>
    </div>
  );
}
