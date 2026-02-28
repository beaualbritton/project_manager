// --- 1. COMPANIES ---
export const mockCompanies = [
  { compID: "c_100", Name: "TechNova Solutions" }
];

// --- 2. EMPLOYEES ---
// Notice how Sarah is a Team Lead, while others are Members.
// Alex is currently unassigned to team_1, making him perfect for the "Team-building/adding" view.
export const mockEmployees = [
  { EmployeeID: "emp_001", Name: "Sarah Chen", Position: "Team Lead", teamIDs: ["team_1"], companyID: "c_100", email: "sarah@technova.com" },
  { EmployeeID: "emp_002", Name: "Marcus Johnson", Position: "Member", teamIDs: ["team_1"], companyID: "c_100", email: "marcus@technova.com" },
  { EmployeeID: "emp_003", Name: "Priya Patel", Position: "Member", teamIDs: ["team_1"], companyID: "c_100", email: "priya@technova.com" },
  { EmployeeID: "emp_004", Name: "Alex Rivera", Position: "Member", teamIDs: ["team_2"], companyID: "c_100", email: "alex@technova.com" },
  { EmployeeID: "emp_005", Name: "Jordan Lee", Position: "Member", teamIDs: [], companyID: "c_100", email: "jordan@technova.com" } // Unassigned!
];

// --- 3. TEAMS ---
export const mockTeams = [
  { teamID: "team_1", Name: "Frontend Core", TaskIDs: ["task_1", "task_2", "task_3"], compID: "c_100", leaderID: "emp_001" },
  { teamID: "team_2", Name: "Backend API", TaskIDs: ["task_4"], compID: "c_100", leaderID: "emp_004" }
];

// --- 4. TASKS ---
// Dates are formatted as ISO strings. 
// task_2 is intentionally OVERDUE to trigger AI warnings.
export const mockTasks = [
  { 
    TaskID: "task_1", 
    Name: "Design System Overhaul", 
    DateTimeStart: "2026-02-20T09:00:00Z", 
    DateTimeEnd: "2026-03-05T17:00:00Z", 
    Budget: 5000, 
    TeamID: "team_1", 
    Status: "in progress" 
  },
  { 
    TaskID: "task_2", 
    Name: "User Authentication UI", 
    DateTimeStart: "2026-02-10T09:00:00Z", 
    DateTimeEnd: "2026-02-25T17:00:00Z", // Past due!
    Budget: 3500, 
    TeamID: "team_1", 
    Status: "active" 
  },
  { 
    TaskID: "task_3", 
    Name: "Dashboard Analytics View", 
    DateTimeStart: "2026-03-01T09:00:00Z", 
    DateTimeEnd: "2026-03-15T17:00:00Z", 
    Budget: 8000, 
    TeamID: "team_1", 
    Status: "active" 
  },
  { 
    TaskID: "task_4", 
    Name: "GraphQL Endpoint Setup", 
    DateTimeStart: "2026-02-25T09:00:00Z", 
    DateTimeEnd: "2026-03-10T17:00:00Z", 
    Budget: 6000, 
    TeamID: "team_2", 
    Status: "in progress" 
  }
]
// Add this to your $lib/mock_data.ts
export const mockSubtasks = [
  { SubtaskID: "st_1", TaskID: "task_1", Title: "Audit existing components", IsComplete: true },
  { SubtaskID: "st_2", TaskID: "task_1", Title: "Draft new color palette", IsComplete: true },
  { SubtaskID: "st_3", TaskID: "task_1", Title: "Update button variants", IsComplete: false },
  { SubtaskID: "st_4", TaskID: "task_1", Title: "Review with design team", IsComplete: false },
  
  { SubtaskID: "st_5", TaskID: "task_2", Title: "Setup JWT middleware", IsComplete: true },
  { SubtaskID: "st_6", TaskID: "task_2", Title: "Create login form UI", IsComplete: false },
  { SubtaskID: "st_7", TaskID: "task_2", Title: "Connect to Django backend", IsComplete: false },
];
