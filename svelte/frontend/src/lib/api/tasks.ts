// src/lib/api/tasks.ts
import { API_URL } from "$lib/config";

async function getCsrf(): Promise<string> {
  const res = await fetch(`${API_URL}/auth/csrf/`, { credentials: "include" });
  const data = await res.json();
  return data.csrfToken;
}

export async function getTasks(employeeId?: string) {
  const url = employeeId
    ? `${API_URL}/tasks/get/?employee_id=${employeeId}`
    : `${API_URL}/tasks/get/`;
  const res = await fetch(url, { credentials: "include" });
  return await res.json();
}

export async function addTask(payload: {
  name: string;
  start_date: string;
  end_date: string;
  budget: number;
  team_id: string;
  status?: string;
}) {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/tasks/add/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  return await res.json();
}

export async function deleteTask(taskId: string) {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/tasks/delete/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify({ task_id: taskId }),
  });
  return await res.json();
}

export async function addSubtask(taskId: string, name: string) {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/subtasks/add/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify({ task_id: taskId, name }),
  });
  return await res.json();
}

export async function deleteSubtask(subtaskId: string) {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/subtasks/delete/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify({ subtask_id: subtaskId }),
  });
  return await res.json();
}

export async function updateSubtaskStatus(subtaskId: string, complete: boolean) {
  const csrf = await getCsrf();
  const res = await fetch(`${API_URL}/subtasks/status/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify({ subtask_id: subtaskId, status: complete ? "COMPLETE" : "INCOMPLETE" }),
  });
  return await res.json();
}
