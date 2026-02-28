<!-- src/routes/tasks/+page.svelte -->
<script lang="ts">
    import { enhance } from '$app/forms';

    let { data, form } = $props();
    let { tasks, stats, defaultTeamId } = data;

    let showModal = $state(false);

    function formatDate(dateString: string) {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short', day: 'numeric', year: 'numeric'
        });
    }

    function isOverdue(endDateString: string) {
        return new Date(endDateString) < new Date();
    }

    $effect(() => {
        if (form?.success) showModal = false;
    });
</script>

<div class="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
    <div class="mx-auto max-w-5xl">

        <header class="mb-8 flex items-end justify-between">
            <div>
                <h1 class="text-3xl font-bold tracking-tight">My Tasks</h1>
            </div>
            <div class="flex items-center gap-4">
                <div class="text-right">
                    <p class="text-sm font-medium text-gray-500 uppercase tracking-wider">Total Active Budget</p>
                    <p class="text-2xl font-bold text-gray-900">${stats?.totalBudget.toLocaleString()}</p>
                </div>
                <button
                    onclick={() => showModal = true}
                    class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
                >
                    + New Task
                </button>
            </div>
        </header>

        <!-- Tasks Grid -->
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {#each tasks as task}
                {@const overdue = isOverdue(task.end_date) && task.status !== 'COMPLETE'}
                <a
                    href="/tasks/{task.taskID}"
                    class="relative flex flex-col rounded-xl border bg-white p-6 shadow-sm transition-all hover:-translate-y-1 hover:shadow-md {overdue ? 'border-red-200' : 'border-gray-200'}"
                >
                    <div class="mb-4 flex items-center justify-between">
                        <span class="inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset
                            {task.status === 'COMPLETE' ? 'bg-green-50 text-green-700 ring-green-600/20' :
                             task.status === 'IN_PROGRESS' ? 'bg-blue-50 text-blue-700 ring-blue-700/10' :
                             'bg-gray-50 text-gray-600 ring-gray-500/10'}">
                            {task.status}
                        </span>
                        {#if overdue}
                            <span class="text-xs font-semibold text-red-600">Overdue</span>
                        {/if}
                    </div>
                    <h3 class="mb-1 text-lg font-semibold text-gray-900">{task.name}</h3>
                    <p class="mb-4 text-sm text-gray-500">Team: {task.team?.name}</p>
                    <div class="mt-auto space-y-3 border-t border-gray-100 pt-4">
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-500">Due Date</span>
                            <span class="font-medium {overdue ? 'text-red-600' : 'text-gray-900'}">{formatDate(task.end_date)}</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-500">Budget</span>
                            <span class="font-medium text-gray-900">${parseFloat(task.budget).toLocaleString()}</span>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    </div>
</div>

<!-- Add Task Modal -->
{#if showModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
        <div class="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
            <div class="mb-6 flex items-center justify-between">
                <h2 class="text-xl font-bold text-gray-900">New Task</h2>
                <button onclick={() => showModal = false} class="text-gray-400 hover:text-gray-600">✕</button>
            </div>

            {#if form?.error}
                <p class="mb-4 text-sm text-red-500">{form.error}</p>
            {/if}

            <form method="POST" action="?/addTask" use:enhance class="space-y-4">
                <input type="hidden" name="team_id" value={defaultTeamId} />

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1" for="name">Task Name</label>
                    <input id="name" name="name" type="text" required
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1" for="start_date">Start Date</label>
                        <input id="start_date" name="start_date" type="datetime-local" required
                            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1" for="end_date">End Date</label>
                        <input id="end_date" name="end_date" type="datetime-local" required
                            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1" for="budget">Budget ($)</label>
                    <input id="budget" name="budget" type="number" min="0" step="0.01" required
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
                </div>

                <div class="flex justify-end gap-3 pt-2">
                    <button type="button" onclick={() => showModal = false}
                        class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
                        Cancel
                    </button>
                    <button type="submit"
                        class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500">
                        Create Task
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}
