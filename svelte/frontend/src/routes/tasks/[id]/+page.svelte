<!-- src/routes/tasks/[id]/+page.svelte -->
<script lang="ts">
    import { updateSubtaskStatus } from '$lib/api/tasks';

    let { data } = $props();
    let { task, team, teamMembers, subtasks, progress } = data;

    function formatDate(dateString: string) {
        return new Date(dateString).toLocaleDateString('en-US', { 
            weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' 
        });
    }

    function isOverdue(endDateString: string) {
        return new Date(endDateString) < new Date();
    }

    let overdue = isOverdue(task.end_date) && task.status !== 'COMPLETE';

    async function toggleSubtask(subtaskId: string, currentStatus: string) {
        const complete = currentStatus !== 'COMPLETE';
        await updateSubtaskStatus(subtaskId, complete);
        // Reload to reflect updated progress
        window.location.reload();
    }
</script>

<div class="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
    <div class="mx-auto max-w-4xl">

        <!-- Breadcrumb -->
        <nav class="mb-6 flex items-center text-sm font-medium text-gray-500">
            <a href="/tasks" class="hover:text-indigo-600 transition-colors">Tasks</a>
            <svg class="mx-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <span class="text-gray-900">{task.taskID}</span>
        </nav>

        <!-- Main Task Header Card -->
        <div class="mb-8 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
            <div class="border-b border-gray-100 p-8">
                <div class="mb-4 flex items-center justify-between">
                    <span class="inline-flex items-center rounded-md px-2.5 py-1 text-xs font-semibold uppercase tracking-wide ring-1 ring-inset
                        {task.status === 'COMPLETE' ? 'bg-green-50 text-green-700 ring-green-600/20' : 
                         task.status === 'IN_PROGRESS' ? 'bg-blue-50 text-blue-700 ring-blue-700/10' : 
                         'bg-gray-50 text-gray-600 ring-gray-500/10'}">
                        {task.status}
                    </span>

                    {#if overdue}
                        <span class="flex items-center rounded-full bg-red-50 px-3 py-1 text-sm font-semibold text-red-600 ring-1 ring-inset ring-red-600/20">
                            <svg class="mr-1.5 h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                            </svg>
                            Overdue
                        </span>
                    {/if}
                </div>

                <h1 class="mb-2 text-3xl font-bold tracking-tight text-gray-900">{task.name}</h1>
                <p class="text-lg text-gray-500">Assigned to <span class="font-medium text-gray-700">{team?.name}</span></p>
            </div>

            <!-- Task Meta Grid -->
            <div class="grid grid-cols-1 divide-y divide-gray-100 bg-gray-50 sm:grid-cols-3 sm:divide-x sm:divide-y-0">
                <div class="p-6">
                    <p class="text-sm font-medium text-gray-500">Start Date</p>
                    <p class="mt-1 font-semibold text-gray-900">{formatDate(task.start_date)}</p>
                </div>
                <div class="p-6">
                    <p class="text-sm font-medium text-gray-500">End Date</p>
                    <p class="mt-1 font-semibold {overdue ? 'text-red-600' : 'text-gray-900'}">{formatDate(task.end_date)}</p>
                </div>
                <div class="p-6">
                    <p class="text-sm font-medium text-gray-500">Budget Allocated</p>
                    <p class="mt-1 font-semibold text-gray-900">${parseFloat(task.budget).toLocaleString()}</p>
                </div>
            </div>
        </div>

        <div class="grid gap-8 lg:grid-cols-3">

            <!-- Left Column: Subtasks -->
            <div class="lg:col-span-2">
                <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <div class="mb-6 flex items-center justify-between">
                        <h2 class="text-xl font-bold text-gray-900">Subtasks</h2>
                        <span class="text-sm font-medium text-gray-500">{progress.completed} of {progress.total} completed</span>
                    </div>

                    <!-- Progress Bar -->
                    <div class="mb-8 h-2.5 w-full overflow-hidden rounded-full bg-gray-100">
                        <div class="h-2.5 rounded-full bg-indigo-600 transition-all duration-500" style="width: {progress.percentage}%"></div>
                    </div>

                    <!-- Checklist -->
                    <div class="space-y-3">
                        {#if subtasks.length === 0}
                            <p class="text-sm text-gray-500 italic">No subtasks defined for this task.</p>
                        {:else}
                            {#each subtasks as subtask}
                                <label class="flex cursor-pointer items-start gap-3 rounded-lg border border-gray-100 p-4 transition-colors hover:bg-gray-50
                                    {subtask.status === 'COMPLETE' ? 'bg-gray-50/50' : 'bg-white'}">
                                    <div class="flex h-6 items-center">
                                        <input 
                                            type="checkbox" 
                                            checked={subtask.status === 'COMPLETE'}
                                            onchange={() => toggleSubtask(subtask.subtaskID, subtask.status)}
                                            class="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600" 
                                        />
                                    </div>
                                    <div class="flex flex-col">
                                        <span class="text-sm font-medium {subtask.status === 'COMPLETE' ? 'text-gray-400 line-through' : 'text-gray-900'}">
                                            {subtask.name}
                                        </span>
                                    </div>
                                </label>
                            {/each}
                        {/if}
                    </div>
                </div>
            </div>

            <!-- Right Column: Team -->
            <div class="lg:col-span-1">
                <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <h2 class="mb-4 text-lg font-bold text-gray-900">Team</h2>
                    {#if team}
                        <p class="text-sm font-semibold text-gray-900">{team.name}</p>
                    {/if}
                </div>
            </div>

        </div>
    </div>
</div>
