// src/routes/+page.server.ts
import type { PageServerLoad } from './$types';
import { mockEmployees, mockTeams, mockTasks } from '$lib/mock_data';

export const load: PageServerLoad = async () => {
    // 1. Identify the user (Team Lead)
    const currentUserId = "emp_001"; 
    const user = mockEmployees.find(e => e.EmployeeID === currentUserId);
    
    // 2. Fetch their teams and tasks
    const userTeams = mockTeams.filter(t => user?.teamIDs.includes(t.teamID));
    const teamIds = userTeams.map(t => t.teamID);
    
    // We'll add a mock "Spent" value to tasks to simulate budget burn for the hackathon
    const tasksWithBurn = mockTasks
        .filter(task => teamIds.includes(task.TeamID))
        .map(task => {
            // Fake budget burn calculation based on status
            let spent = 0;
            if (task.Status === 'complete') spent = task.Budget;
            else if (task.Status === 'in progress') spent = task.Budget * 0.75;
            else spent = task.Budget * 0.1; // active/todo
            
            return { ...task, Spent: spent };
        });

    // 3. Calculate Top Zone Snapshot Numbers
    const totalTasks = tasksWithBurn.length;
    const activeTasks = tasksWithBurn.filter(t => t.Status !== 'complete').length;
    
    const totalBudget = tasksWithBurn.reduce((sum, t) => sum + t.Budget, 0);
    const totalSpent = tasksWithBurn.reduce((sum, t) => sum + t.Spent, 0);
    const budgetUtilization = totalBudget > 0 ? Math.round((totalSpent / totalBudget) * 100) : 0;
    
    // Headcount: Unique employees across all the lead's teams
    const headcount = mockEmployees.filter(e => e.teamIDs.some(id => teamIds.includes(id))).length;

    // 4. Generate a mock Activity Feed (Right Column)
    // In Django, this would be a simple `ActivityLog.objects.order_by('-timestamp')[:5]`
    const activityFeed = [
        { id: 1, user: "Marcus Johnson", action: "moved", task: "User Authentication UI", to: "In Progress", time: "2 hours ago" },
        { id: 2, user: "Sarah Chen", action: "commented on", task: "Design System Overhaul", time: "4 hours ago" },
        { id: 3, user: "Priya Patel", action: "completed subtask in", task: "Dashboard Analytics View", time: "Yesterday" },
        { id: 4, user: "System", action: "flagged", task: "User Authentication UI", to: "Overdue", time: "Yesterday" },
    ];

    // 5. The AI Insights (Bottom Zone)
    // In reality, you would call Gemini here passing `tasksWithBurn` as context.
    // We mock the response here so your UI works immediately.
    const aiInsights = [
        "User Authentication UI is past its deadline and has burned 75% of its budget. Marcus Johnson may need assistance.",
        "Frontend Core team is running at 68% total budget utilization, which is healthy for this stage of the sprint.",
        "Design System Overhaul is progressing well but has a high remaining budget ($1,250) that could be reallocated if needed."
    ];

    return {
        user,
        stats: { totalTasks, activeTasks, budgetUtilization, headcount },
        tasks: tasksWithBurn,
        activityFeed,
        aiInsights
    };
};
