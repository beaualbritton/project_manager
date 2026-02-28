<!-- src/routes/+page.svelte -->
<script lang="ts">
    let { data } = $props();
    let { user, stats, tasks, activityFeed, aiInsights } = data;

    // For the freeform AI query box
    let aiQuery = $state('');
    let isQuerying = $state(false);

    function isOverdue(endDateString: string) {
        return new Date(endDateString) < new Date();
    }

    async function handleAIQuery() {
        if (!aiQuery.trim()) return;
        isQuerying = true;
        // In a real app, this would hit a SvelteKit API route that calls Gemini
        setTimeout(() => {
            alert(`Hackathon Demo: You asked "${aiQuery}". Gemini would return a custom insight here!`);
            isQuerying = false;
            aiQuery = '';
        }, 1000);
    }
</script>

<div class="min-h-screen bg-gray-100 p-4 md:p-8 font-sans text-gray-900">
    <div class="mx-auto max-w-6xl">
        
        <!-- Navigation / Header -->
        <header class="mb-8 flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-bold tracking-tight text-gray-900">Lead Dashboard</h1>
                <p class="text-sm text-gray-500">Welcome back, {user?.Name}</p>
            </div>
            <nav class="flex gap-4">
                <a href="/" class="rounded-md bg-white px-3 py-2 text-sm font-medium text-indigo-600 shadow-sm ring-1 ring-inset ring-gray-300">Dashboard</a>
                <a href="/tasks" class="rounded-md px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50">Tasks</a>
                <!-- Placeholder for the standalone Gemini view -->
                <a href="/analytics" class="rounded-md px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 flex items-center gap-1">
                    <svg class="h-4 w-4 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                    Analytics
                </a>
            </nav>
        </header>

        <!-- ZONE 1: Snapshot Row -->
        <div class="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
            <div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Total Tasks</p>
                <p class="mt-2 text-3xl font-bold text-gray-900">{stats.totalTasks}</p>
            </div>
            <div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Active / In-Progress</p>
                <p class="mt-2 text-3xl font-bold text-indigo-600">{stats.activeTasks}</p>
            </div>
            <div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Budget Utilized</p>
                <div class="mt-2 flex items-baseline gap-2">
                    <p class="text-3xl font-bold {stats.budgetUtilization > 80 ? 'text-red-600' : 'text-gray-900'}">
                        {stats.budgetUtilization}%
                    </p>
                    {#if stats.budgetUtilization > 80}
                        <span class="text-xs font-medium text-red-600 flex items-center"><svg class="h-3 w-3 mr-0.5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" /></svg> High</span>
                    {/if}
                </div>
            </div>
            <div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Team Headcount</p>
                <p class="mt-2 text-3xl font-bold text-gray-900">{stats.headcount}</p>
            </div>
        </div>

        <!-- ZONE 2: Two Columns (Table & Feed) -->
        <div class="mb-8 grid gap-8 lg:grid-cols-3">
            
            <!-- Left: Task Table (Condensed) -->
            <div class="lg:col-span-2 rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
                <div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
                    <h2 class="text-base font-semibold text-gray-900">Active Tasks</h2>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm text-gray-600">
                        <thead class="bg-white text-xs uppercase text-gray-500 border-b border-gray-100">
                            <tr>
                                <th class="px-6 py-3 font-medium">Task Name</th>
                                <th class="px-6 py-3 font-medium">Status</th>
                                <th class="px-6 py-3 font-medium">Budget Burn</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            {#each tasks as task}
                                {@const overdue = isOverdue(task.DateTimeEnd) && task.Status !== 'complete'}
                                {@const burnPct = Math.round((task.Spent / task.Budget) * 100)}
                                
                                <tr class="hover:bg-gray-50 transition-colors group cursor-pointer" onclick={() => window.location.href=`/tasks/${task.TaskID}`}>
                                    <td class="px-6 py-4">
                                        <div class="font-medium {overdue ? 'text-red-600' : 'text-gray-900'}">{task.Name}</div>
                                        {#if overdue}
                                            <div class="text-xs text-red-500 mt-0.5">Overdue</div>
                                        {/if}
                                    </td>
                                    <td class="px-6 py-4">
                                        <span class="inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset
                                            {task.Status === 'complete' ? 'bg-green-50 text-green-700 ring-green-600/20' : 
                                             task.Status === 'in progress' ? 'bg-blue-50 text-blue-700 ring-blue-700/10' : 
                                             'bg-gray-50 text-gray-600 ring-gray-500/10'}">
                                            {task.Status}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4">
                                        <div class="flex items-center gap-2">
                                            <div class="w-full bg-gray-200 rounded-full h-2 max-w-[80px]">
                                                <div class="h-2 rounded-full {burnPct > 90 ? 'bg-red-500' : 'bg-indigo-500'}" style="width: {burnPct}%"></div>
                                            </div>
                                            <span class="text-xs font-medium {burnPct > 90 ? 'text-red-600' : 'text-gray-600'}">{burnPct}%</span>
                                        </div>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Right: Activity Feed -->
            <div class="lg:col-span-1 rounded-xl border border-gray-200 bg-white shadow-sm flex flex-col">
                <div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
                    <h2 class="text-base font-semibold text-gray-900">Recent Activity</h2>
                </div>
                <div class="p-6 flex-1">
                    <ul class="space-y-5">
                        {#each activityFeed as item}
                            <li class="relative flex gap-4">
                                <!-- Timeline line -->
                                <div class="absolute left-1.5 top-5 -bottom-5 w-px bg-gray-200 last:hidden"></div>
                                
                                <div class="relative mt-1 flex h-3 w-3 flex-none items-center justify-center rounded-full bg-gray-100 ring-4 ring-white">
                                    <div class="h-1.5 w-1.5 rounded-full {item.user === 'System' ? 'bg-red-500' : 'bg-gray-400'}"></div>
                                </div>
                                <div class="flex-auto text-sm">
                                    <p class="text-gray-600">
                                        <span class="font-medium text-gray-900">{item.user}</span> 
                                        {item.action} 
                                        <span class="font-medium text-gray-900">{item.task}</span>
                                        {#if item.to}
                                            to <span class="font-medium text-indigo-600">{item.to}</span>
                                        {/if}
                                    </p>
                                    <p class="mt-0.5 text-xs text-gray-400">{item.time}</p>
                                </div>
                            </li>
                        {/each}
                    </ul>
                </div>
            </div>
        </div>

        <!-- ZONE 3: AI Insight Card -->
        <div class="rounded-xl border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-white shadow-sm overflow-hidden">
            <div class="border-b border-purple-100 px-6 py-4 flex items-center gap-2">
                <svg class="h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <h2 class="text-base font-bold text-purple-900">Gemini Project Insights</h2>
            </div>
            
            <div class="p-6">
                <ul class="space-y-3 mb-6">
                    {#each aiInsights as insight}
                        <li class="flex items-start gap-3 text-sm text-gray-800">
                            <div class="mt-1 h-1.5 w-1.5 flex-none rounded-full bg-purple-500"></div>
                            <p>{insight}</p>
                        </li>
                    {/each}
                </ul>

                <!-- Freeform Query Box -->
                <form onsubmit={(e) => { e.preventDefault(); handleAIQuery(); }} class="mt-4 flex gap-3">
                    <input 
                        type="text" 
                        bind:value={aiQuery}
                        placeholder="Ask Gemini about your budget, team capacity, or risks..." 
                        class="block w-full rounded-lg border-0 py-2.5 pl-4 text-gray-900 shadow-sm ring-1 ring-inset ring-purple-200 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-purple-600 sm:text-sm sm:leading-6"
                    >
                    <button 
                        type="submit" 
                        disabled={isQuerying || !aiQuery.trim()}
                        class="flex-none rounded-lg bg-purple-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-purple-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-purple-600 disabled:opacity-50"
                    >
                        {isQuerying ? 'Thinking...' : 'Ask AI'}
                    </button>
                </form>
            </div>
        </div>

    </div>
</div>
