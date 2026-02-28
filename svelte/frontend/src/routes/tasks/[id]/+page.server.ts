// src/routes/tasks/[id]/+page.server.ts
import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { API_URL } from '$lib/config';

export const load: PageServerLoad = async ({ fetch, cookies, params }) => {
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');

  const res = await fetch(`${API_URL}/tasks/get/`, {
    headers: {
      'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`
    }
  });

  if (!res.ok) throw redirect(302, '/login');

  const data = await res.json();
  const task = (data.tasks ?? []).find((t: any) => t.taskID === params.id);
  if (!task) throw error(404, { message: 'Task not found' });

  const subtasks = task.subtasks ?? [];
  const completedSubtasks = subtasks.filter((s: any) => s.status === 'COMPLETE').length;

  return {
    task,
    team: task.team ?? null,
    teamMembers: [],
    subtasks,
    progress: {
      percentage: subtasks.length > 0 ? Math.round((completedSubtasks / subtasks.length) * 100) : 0,
      completed: completedSubtasks,
      total: subtasks.length
    }
  };
};
