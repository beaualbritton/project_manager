// src/routes/analytics/+page.server.ts
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { API_URL } from '$lib/config';

interface InsightCategory {
  category: 'Budget Risk' | 'Scheduling' | 'Team Performance';
  headline: string;
  detail: string;
  severity: 'low' | 'medium' | 'high';
  isAllClear: boolean;
}

const FALLBACK_INSIGHTS: InsightCategory[] = [
  { category: 'Budget Risk', headline: 'Could not load insight', detail: 'Gemini did not respond. Check your API key.', severity: 'low', isAllClear: false },
  { category: 'Scheduling', headline: 'Could not load insight', detail: 'Gemini did not respond. Check your API key.', severity: 'low', isAllClear: false },
  { category: 'Team Performance', headline: 'Could not load insight', detail: 'Gemini did not respond. Check your API key.', severity: 'low', isAllClear: false },
];

export const load: PageServerLoad = async ({ fetch, cookies }) => {
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');
  const headers = { 'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}` };

  // Fetch tasks for context
  const tasksRes = await fetch(`${API_URL}/tasks/get/`, { headers });
  if (!tasksRes.ok) throw redirect(302, '/login');
  const tasksData = await tasksRes.json();
  const tasks = tasksData.tasks ?? [];

  const taskContext = JSON.stringify(tasks.map((t: any) => ({
    name: t.name,
    status: t.status,
    budget: t.budget,
    end_date: t.end_date,
    team: t.team?.name,
    subtasks_total: t.subtasks?.length ?? 0,
    subtasks_complete: t.subtasks?.filter((s: any) => s.status === 'COMPLETE').length ?? 0,
  })));

  const prompt = `You are a project management analyst. Given these tasks: ${taskContext}

Return ONLY a valid JSON array with exactly 3 objects. No markdown, no explanation, just the array.
Each object must have these exact fields:
- category: one of "Budget Risk", "Scheduling", or "Team Performance"
- headline: short title string
- detail: 1-2 sentence explanation string  
- severity: one of "low", "medium", or "high"
- isAllClear: boolean, true only if there are no issues in this category

Example format:
[{"category":"Budget Risk","headline":"...","detail":"...","severity":"medium","isAllClear":false},...]`;

  let insights: InsightCategory[] = FALLBACK_INSIGHTS;

  try {
    const geminiRes = await fetch(`${API_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken ?? '',
        'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`
      },
      body: JSON.stringify({ prompt })
    });

    if (geminiRes.ok) {
      const geminiData = await geminiRes.json();
      const raw = geminiData.answer ?? '';
      const clean = raw.replace(/```json|```/g, '').trim();
      const parsed = JSON.parse(clean);
      if (Array.isArray(parsed) && parsed.length === 3) {
        insights = parsed;
      }
    }
  } catch {
    insights = FALLBACK_INSIGHTS;
  }

  return { insights, taskContext };
};
