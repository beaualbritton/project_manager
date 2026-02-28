<!-- src/routes/tasks/[id]/+page.svelte -->
<script lang="ts">
    import { enhance } from '$app/forms';

    let { data, form } = $props();
    let { task, team, subtasks, progress } = data;

    function formatDate(dateString: string) {
        return new Date(dateString).toLocaleDateString('en-US', {
            weekday: 'short', month: 'short', day: 'numeric', year: 'numeric'
        });
    }

    function isOverdue(endDateString: string) {
        return new Date(endDateString) < new Date();
    }

    let overdue = isOverdue(task.end_date) && task.status !== 'COMPLETE';
</script>

<div class="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
    <div class="mx-auto max-w-4xl">

        <nav class="mb-6 flex items-center text-sm font-medium text-gray-500">
            <a href="/tasks" class="hover:text-indigo-600 transition-colors">Tasks</a>
            <svg class="mx-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <span class="text-gray-900">{task.name}</span>
        </nav>

        <!-- Task Header -->
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
                        <span class="rounded-full bg-red-50 px-3 py-1 text-sm font-semibold text-red-600 ring-1 ring-inset ring-red-600/20">
                            Overdue
                        </span>
                    {/if}
                </div>
                <h1 class="mb-2 text-3xl font-bold tracking-tight text-gray-900">{task.name}</h1>
                <p class="text-lg text-gray-500">Team: <span class="font-medium text-gray-700">{team?.name}</span></p>
            </div>
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
                    <p class="text-sm font-medium text-gray-500">Budget</p>
                    <p class="mt-1 font-semibold text-gray-900">${parseFloat(task.budget).toLocaleString()}</p>
                </div>
            </div>
        </div>

        <!-- Subtasks -->
        <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <div class="mb-6 flex items-center justify-between">
                <h2 class="text-xl font-bold text-gray-900">Subtasks</h2>
                <span class="text-sm font-medium text-gray-500">{progress.completed} of {progress.total} completed</span>
            </div>

            <div class="mb-8 h-2.5 w-full overflow-hidden rounded-full bg-gray-100">
                <div class="h-2.5 rounded-full bg-indigo-600 transition-all duration-500" style="width: {progress.percentage}%"></div>
            </div>

            <div class="space-y-3 mb-6">
                {#if subtasks.length === 0}
                    <p class="text-sm text-gray-500 italic">No subtasks yet.</p>
                {:else}
                    {#each subtasks as subtask}
                        <div class="flex items-center gap-3 rounded-lg border border-gray-100 p-4 transition-colors hover:bg-gray-50
                            {subtask.status === 'COMPLETE' ? 'bg-gray-50/50' : 'bg-white'}">
                            <form method="POST" action="?/toggleSubtask" use:enhance>
                                <input type="hidden" name="subtask_id" value={subtask.subtaskID} />
                                <input type="hidden" name="current_status" value={subtask.status} />
                                <button type="submit"
                                    class="h-5 w-5 rounded border-2 flex items-center justify-center transition-colors
                                        {subtask.status === 'COMPLETE' ? 'border-indigo-600 bg-indigo-600' : 'border-gray-300 bg-white'}">
                                    {#if subtask.status === 'COMPLETE'}
                                        <svg class="h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                                        </svg>
                                    {/if}
                                </button>
                            </form>
                            <span class="text-sm font-medium {subtask.status === 'COMPLETE' ? 'text-gray-400 line-through' : 'text-gray-900'}">
                                {subtask.name}
                            </span>
                        </div>
                    {/each}
                {/if}
            </div>

            <!-- Add Subtask -->
            {#if form?.error}
                <p class="mb-2 text-sm text-red-500">{form.error}</p>
            {/if}
            <form method="POST" action="?/addSubtask" use:enhance class="flex gap-3">
                <input
                    type="text"
                    name="name"
                    placeholder="Add a subtask..."
                    class="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <button type="submit"
                    class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500">
                    Add
                </button>
            </form>
        </div>

    </div>
</div>
