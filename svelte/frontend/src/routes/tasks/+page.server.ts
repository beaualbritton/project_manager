// src/routes/tasks/+page.server.ts
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { API_URL } from '$lib/config';

export const load: PageServerLoad = async ({ fetch, cookies }) => {
  console.log('cookies:', cookies.getAll());  //
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');

  const res = await fetch(`${API_URL}/tasks/get/`, {
    headers: {
      'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`
    }
  });

  if (!res.ok) throw redirect(302, '/login');

  const data = await res.json();
  const tasks = data.tasks ?? [];
  const totalBudget = tasks.reduce((sum: number, t: any) => sum + parseFloat(t.budget), 0);
  const activeTasksCount = tasks.filter((t: any) => t.status === 'ACTIVE' || t.status === 'IN_PROGRESS').length;

  return {
    tasks,
    stats: { totalBudget, activeTasksCount }
  };
};
