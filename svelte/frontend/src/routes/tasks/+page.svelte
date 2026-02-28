<script lang="ts">
    let { data } = $props();
    let { tasks, stats } = data;

    function formatDate(dateString: string) {
        return new Date(dateString).toLocaleDateString('en-US', { 
            month: 'short', day: 'numeric', year: 'numeric' 
        });
    }

    function isOverdue(endDateString: string) {
        return new Date(endDateString) < new Date();
    }
</script>

<div class="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
    <div class="mx-auto max-w-5xl">

        <!-- Header Section -->
        <header class="mb-8 flex items-end justify-between">
            <div>
                <h1 class="text-3xl font-bold tracking-tight">My Tasks</h1>
            </div>
            <div class="text-right">
                <p class="text-sm font-medium text-gray-500 uppercase tracking-wider">Total Active Budget</p>
                <p class="text-2xl font-bold text-gray-900">${stats?.totalBudget.toLocaleString()}</p>
            </div>
        </header>

        <!-- Tasks Grid -->
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {#each tasks as task}
                {@const overdue = isOverdue(task.end_date) && task.status !== 'COMPLETE'}

                <a 
                    href="/tasks/{task.taskID}" 
                    class="relative flex flex-col rounded-xl border bg-white p-6 shadow-sm transition-all hover:-translate-y-1 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 {overdue ? 'border-red-200' : 'border-gray-200'}"
                >
                    <!-- Status Badge -->
                    <div class="mb-4 flex items-center justify-between">
                        <span class="inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset
                            {task.status === 'COMPLETE' ? 'bg-green-50 text-green-700 ring-green-600/20' : 
                             task.status === 'IN_PROGRESS' ? 'bg-blue-50 text-blue-700 ring-blue-700/10' : 
                             'bg-gray-50 text-gray-600 ring-gray-500/10'}">
                            {task.status}
                        </span>

                        {#if overdue}
                            <span class="flex items-center text-xs font-semibold text-red-600">
                                <svg class="mr-1 h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                                </svg>
                                Overdue
                            </span>
                        {/if}
                    </div>

                    <!-- Task Details -->
                    <h3 class="mb-1 text-lg font-semibold text-gray-900">{task.name}</h3>
                    <p class="mb-4 text-sm text-gray-500">Team: {task.team?.name}</p>

                    <div class="mt-auto space-y-3 border-t border-gray-100 pt-4">
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-500">Due Date</span>
                            <span class="font-medium {overdue ? 'text-red-600' : 'text-gray-900'}">
                                {formatDate(task.end_date)}
                            </span>
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
