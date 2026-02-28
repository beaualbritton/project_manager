// src/routes/+page.server.ts
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { API_URL } from '$lib/config';

export const load: PageServerLoad = async ({ fetch, cookies }) => {
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');
  const headers = { 'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}` };

  const res = await fetch(`${API_URL}/tasks/get/`, { headers });
  if (!res.ok) throw redirect(302, '/login');

  const data = await res.json();

  const tasks = (data.tasks ?? []).map((task: any) => {
    let spent = 0;
    if (task.status === 'COMPLETE') spent = parseFloat(task.budget);
    else if (task.status === 'IN_PROGRESS') spent = parseFloat(task.budget) * 0.75;
    else spent = parseFloat(task.budget) * 0.1;
    return { ...task, spent };
  });

  const totalTasks = tasks.length;
  const activeTasks = tasks.filter((t: any) => t.status !== 'COMPLETE').length;
  const totalBudget = tasks.reduce((sum: number, t: any) => sum + parseFloat(t.budget), 0);
  const totalSpent = tasks.reduce((sum: number, t: any) => sum + t.spent, 0);
  const budgetUtilization = totalBudget > 0 ? Math.round((totalSpent / totalBudget) * 100) : 0;

  return {
    stats: { totalTasks, activeTasks, budgetUtilization },
    tasks,
    activityFeed: []
  };
};;
