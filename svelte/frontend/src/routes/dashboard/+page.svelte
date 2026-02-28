<!-- src/routes/dashboard/+page.svelte -->
<script lang="ts">
    let { data } = $props();
    let { stats, tasks, activityFeed } = data;

    function isOverdue(endDateString: string) {
        return new Date(endDateString) < new Date();
    }
</script>

<div class="min-h-screen bg-gray-100 p-4 md:p-8 font-sans text-gray-900">
    <div class="mx-auto max-w-6xl">

        <header class="mb-8">
            <h1 class="text-2xl font-bold tracking-tight text-gray-900">Lead Dashboard</h1>
        </header>

        <!-- Snapshot Row -->
        <div class="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-3">
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
                        <span class="text-xs font-medium text-red-600">⚠ High</span>
                    {/if}
                </div>
            </div>
        </div>

        <!-- Task Table + Activity Feed -->
        <div class="grid gap-8 lg:grid-cols-3">

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
                                {@const overdue = isOverdue(task.end_date) && task.status !== 'COMPLETE'}
                                {@const burnPct = Math.min(Math.round((task.spent / parseFloat(task.budget)) * 100), 100)}
                                <tr class="hover:bg-gray-50 transition-colors cursor-pointer" onclick={() => window.location.href=`/tasks/${task.taskID}`}>
                                    <td class="px-6 py-4">
                                        <div class="font-medium {overdue ? 'text-red-600' : 'text-gray-900'}">{task.name}</div>
                                        {#if overdue}<div class="text-xs text-red-500 mt-0.5">Overdue</div>{/if}
                                    </td>
                                    <td class="px-6 py-4">
                                        <span class="inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset
                                            {task.status === 'COMPLETE' ? 'bg-green-50 text-green-700 ring-green-600/20' :
                                             task.status === 'IN_PROGRESS' ? 'bg-blue-50 text-blue-700 ring-blue-700/10' :
                                             'bg-gray-50 text-gray-600 ring-gray-500/10'}">
                                            {task.status}
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

            <!-- Activity Feed -->
            <div class="lg:col-span-1 rounded-xl border border-gray-200 bg-white shadow-sm flex flex-col">
                <div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
                    <h2 class="text-base font-semibold text-gray-900">Recent Activity</h2>
                </div>
                <div class="p-6 flex-1">
                    {#if activityFeed.length === 0}
                        <p class="text-sm text-gray-400 italic">No recent activity.</p>
                    {:else}
                        <ul class="space-y-5">
                            {#each activityFeed as item}
                                <li class="relative flex gap-4">
                                    <div class="relative mt-1 flex h-3 w-3 flex-none items-center justify-center rounded-full bg-gray-100 ring-4 ring-white">
                                        <div class="h-1.5 w-1.5 rounded-full {item.user === 'System' ? 'bg-red-500' : 'bg-gray-400'}"></div>
                                    </div>
                                    <div class="flex-auto text-sm">
                                        <p class="text-gray-600">
                                            <span class="font-medium text-gray-900">{item.user}</span>
                                            {item.action}
                                            <span class="font-medium text-gray-900">{item.task}</span>
                                            {#if item.to}to <span class="font-medium text-indigo-600">{item.to}</span>{/if}
                                        </p>
                                        <p class="mt-0.5 text-xs text-gray-400">{item.time}</p>
                                    </div>
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </div>
            </div>

        </div>
    </div>
</div>
