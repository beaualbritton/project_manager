import type { PageServerLoad } from './$types';
// Import from your $lib folder
import { mockEmployees, mockTeams, mockTasks } from '$lib/mock_data';

export const load: PageServerLoad = async ({ cookies }) => {
    // 1. Simulate getting the logged-in user
    const currentUserId = "emp_001"; 

    // 2. Fetch the user's data
    const user = mockEmployees.find(e => e.EmployeeID === currentUserId);
    
    if (!user) {
        return { status: 404, error: 'User not found' };
    }

    // 3. Fetch the teams the user belongs to
    const userTeams = mockTeams.filter(t => user.teamIDs.includes(t.teamID));

    // 4. Fetch the tasks for those teams
    const teamIds = userTeams.map(t => t.teamID);
    const userTasks = mockTasks.filter(task => teamIds.includes(task.TeamID));

    // 5. Calculate some basic stats for the view
    const totalBudget = userTasks.reduce((sum, task) => sum + task.Budget, 0);
    const activeTasksCount = userTasks.filter(t => t.Status === 'active' || t.Status === 'in progress').length;

    // 6. Return the data to the Svelte component
    return {
        user,
        teams: userTeams,
        tasks: userTasks,
        stats: {
            totalBudget,
            activeTasksCount
        }
    };
};;
