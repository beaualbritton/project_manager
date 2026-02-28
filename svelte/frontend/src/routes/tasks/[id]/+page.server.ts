// src/routes/tasks/[id]/+page.server.ts
import { error, redirect, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { API_URL } from '$lib/config';

export const load: PageServerLoad = async ({ fetch, cookies, params }) => {
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');
  const headers = { 'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}` };

  const res = await fetch(`${API_URL}/tasks/get/`, { headers });
  if (!res.ok) throw redirect(302, '/login');

  const data = await res.json();
  const task = (data.tasks ?? []).find((t: any) => t.taskID === params.id);
  if (!task) throw error(404, { message: 'Task not found' });

  const subtasks = task.subtasks ?? [];
  const completedSubtasks = subtasks.filter((s: any) => s.status === 'COMPLETE').length;

  return {
    task,
    team: task.team ?? null,
    subtasks,
    progress: {
      percentage: subtasks.length > 0 ? Math.round((completedSubtasks / subtasks.length) * 100) : 0,
      completed: completedSubtasks,
      total: subtasks.length
    }
  };
};

export const actions: Actions = {
  addSubtask: async ({ request, fetch, cookies, params }) => {
    const sessionid = cookies.get('sessionid');
    const csrftoken = cookies.get('csrftoken');

    const form = await request.formData();
    const name = form.get('name') as string;

    if (!name?.trim()) return fail(400, { error: 'Subtask name is required' });

    const res = await fetch(`${API_URL}/subtasks/add/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken ?? '',
        'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`
      },
      body: JSON.stringify({ task_id: params.id, name })
    });

    if (!res.ok) return fail(400, { error: 'Failed to add subtask' });
    return { success: true };
  },

  toggleSubtask: async ({ request, fetch, cookies }) => {
    const sessionid = cookies.get('sessionid');
    const csrftoken = cookies.get('csrftoken');

    const form = await request.formData();
    const subtask_id = form.get('subtask_id') as string;
    const current_status = form.get('current_status') as string;
    const newStatus = current_status === 'COMPLETE' ? 'INCOMPLETE' : 'COMPLETE';

    const res = await fetch(`${API_URL}/subtasks/status/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken ?? '',
        'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`
      },
      body: JSON.stringify({ subtask_id, status: newStatus })
    });

    if (!res.ok) return fail(400, { error: 'Failed to update subtask' });
    return { success: true };
  }
};
