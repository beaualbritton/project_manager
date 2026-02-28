// src/routes/api/gemini-query/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { API_URL } from '$lib/config';

export const POST: RequestHandler = async ({ request, fetch, cookies }) => {
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');

  const { query, taskContext } = await request.json();

  const prompt = `You are a project management analyst. Here is the current task data: ${taskContext}

The user asks: "${query}"

Reply in 2-3 sentences max. Be specific and reference actual task names or numbers where relevant.`;

  const res = await fetch(`${API_URL}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken ?? '',
      'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`
    },
    body: JSON.stringify({ prompt })
  });

  if (!res.ok) return json({ answer: 'Gemini is unavailable right now.' });

  const data = await res.json();
  return json({ answer: data.answer ?? 'No response.' });
};
