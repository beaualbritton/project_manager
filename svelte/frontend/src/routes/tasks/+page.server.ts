// src/routes/tasks/+page.server.ts
import { redirect, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { API_URL } from '$lib/config';

export const load: PageServerLoad = async ({ fetch, cookies }) => {
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');
  const headers = { 'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}` };

  // Fetch tasks
  const tasksRes = await fetch(`${API_URL}/tasks/get/`, { headers });
  if (!tasksRes.ok) throw redirect(302, '/login');
  const tasksData = await tasksRes.json();
  const tasks = tasksData.tasks ?? [];

  // Fetch current employee to get their first team_id
  const empRes = await fetch(`${API_URL}/employees/get/`, { headers });
  const empData = empRes.ok ? await empRes.json() : [];
  const employee = empData[0] ?? null;
  const defaultTeamId = employee?.teamIDs?.[0] ?? null;

  const totalBudget = tasks.reduce((sum: number, t: any) => sum + parseFloat(t.budget), 0);
  const activeTasksCount = tasks.filter((t: any) => t.status === 'ACTIVE' || t.status === 'IN_PROGRESS').length;

  return {
    tasks,
    defaultTeamId,
    stats: { totalBudget, activeTasksCount }
  };
};

export const actions: Actions = {
  addTask: async ({ request, fetch, cookies }) => {
    const sessionid = cookies.get('sessionid');
    const csrftoken = cookies.get('csrftoken');

    const form = await request.formData();
    const name = form.get('name') as string;
    const start_date = form.get('start_date') as string;
    const end_date = form.get('end_date') as string;
    const budget = form.get('budget') as string;
    const team_id = form.get('team_id') as string;

    const res = await fetch(`${API_URL}/tasks/add/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken ?? '',
        'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`
      },
      body: JSON.stringify({ name, start_date, end_date, budget: parseFloat(budget), team_id })
    });

    if (!res.ok) return fail(400, { error: 'Failed to create task' });
    return { success: true };
  }
};
