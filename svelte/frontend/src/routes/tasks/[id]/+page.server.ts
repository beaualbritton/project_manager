// src/routes/tasks/[id]/+page.server.ts
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { mockTasks, mockTeams, mockEmployees, mockSubtasks } from '$lib/mock_data';

export const load: PageServerLoad = async ({ params }) => {
    // 1. Get the ID from the URL (e.g., "task_1")
    const taskId = params.id;

    // 2. Find the specific task
    const task = mockTasks.find(t => t.TaskID === taskId);
    
    // If the task doesn't exist, throw a 404
    if (!task) {
        throw error(404, { message: 'Task not found' });
    }

    // 3. Get related data to make the view rich
    const team = mockTeams.find(t => t.teamID === task.TeamID);
    
    // Find all employees assigned to this team
    const teamMembers = mockEmployees.filter(e => e.teamIDs.includes(task.TeamID));
    
    // 4. Get the subtasks/checklist items for this specific task
    const subtasks = mockSubtasks.filter(st => st.TaskID === taskId);

    // Calculate progress percentage
    const completedSubtasks = subtasks.filter(st => st.IsComplete).length;
    const progressPercentage = subtasks.length > 0 
        ? Math.round((completedSubtasks / subtasks.length) * 100) 
        : 0;

    return {
        task,
        team,
        teamMembers,
        subtasks,
        progress: {
            percentage: progressPercentage,
            completed: completedSubtasks,
            total: subtasks.length
        }
    };
};
