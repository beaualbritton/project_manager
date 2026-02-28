<!-- src/routes/analytics/+page.svelte -->
<script lang="ts">
    import type { PageData } from './$types';

    let { data }: { data: PageData } = $props();
    let { insights, taskContext } = data;

    let query = $state('');
    let isQuerying = $state(false);
    let chatResponse = $state<string | null>(null);

    function getSeverityStyles(severity: string, isAllClear: boolean) {
        if (isAllClear) return 'bg-emerald-50 border-emerald-200 text-emerald-900';
        switch (severity) {
            case 'high': return 'bg-red-50 border-red-200 text-red-900';
            case 'medium': return 'bg-amber-50 border-amber-200 text-amber-900';
            case 'low': return 'bg-blue-50 border-blue-200 text-blue-900';
            default: return 'bg-gray-50 border-gray-200 text-gray-900';
        }
    }

    function getBadgeStyles(severity: string, isAllClear: boolean) {
        if (isAllClear) return 'bg-emerald-100 text-emerald-800 ring-emerald-600/20';
        switch (severity) {
            case 'high': return 'bg-red-100 text-red-800 ring-red-600/20';
            case 'medium': return 'bg-amber-100 text-amber-800 ring-amber-600/20';
            case 'low': return 'bg-blue-100 text-blue-800 ring-blue-600/20';
            default: return 'bg-gray-100 text-gray-800 ring-gray-600/20';
        }
    }

    async function handleQuery() {
        if (!query.trim()) return;
        isQuerying = true;
        chatResponse = null;

        try {
            const res = await fetch('/api/gemini-query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, taskContext })
            });
            const data = await res.json();
            chatResponse = data.answer ?? 'No response.';
        } catch {
            chatResponse = 'Error contacting Gemini.';
        }

        isQuerying = false;
        query = '';
    }
</script>

<div class="min-h-screen bg-white p-4 md:p-8 font-sans text-gray-900">
    <div class="mx-auto max-w-4xl">

        <header class="mb-10 border-b border-gray-100 pb-6">
            <div class="flex items-center gap-3 mb-2">
                <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-100 text-purple-600">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                </div>
                <h1 class="text-3xl font-bold tracking-tight text-gray-900">AI Analyst Briefing</h1>
            </div>
            <p class="text-lg text-gray-500">Generated based on your live project data.</p>
        </header>

        <!-- Insight Cards -->
        <div class="mb-16 space-y-6">
            {#each insights as insight}
                <div class="relative rounded-2xl border p-6 {getSeverityStyles(insight.severity, insight.isAllClear)}">
                    <div class="mb-3 flex items-start justify-between">
                        <h2 class="text-sm font-bold uppercase tracking-wider opacity-80">{insight.category}</h2>
                        <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ring-1 ring-inset {getBadgeStyles(insight.severity, insight.isAllClear)}">
                            {insight.isAllClear ? 'All Clear' : `${insight.severity.charAt(0).toUpperCase() + insight.severity.slice(1)} Risk`}
                        </span>
                    </div>

                    {#if insight.isAllClear}
                        <div class="flex items-center gap-3">
                            <svg class="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p class="text-lg font-medium text-emerald-900">{insight.headline}</p>
                        </div>
                        <p class="mt-2 text-emerald-800/80 leading-relaxed">{insight.detail}</p>
                    {:else}
                        <h3 class="mb-2 text-xl font-bold leading-tight">{insight.headline}</h3>
                        <p class="text-base leading-relaxed opacity-90">{insight.detail}</p>
                    {/if}
                </div>
            {/each}
        </div>

        <!-- Freeform Query -->
        <div class="border-t border-gray-100 pt-10">
            <h2 class="mb-6 text-xl font-bold text-gray-900">Ask follow-up questions</h2>

            <form onsubmit={(e) => { e.preventDefault(); handleQuery(); }} class="relative">
                <div class="overflow-hidden rounded-2xl border border-gray-300 shadow-sm focus-within:border-purple-500 focus-within:ring-1 focus-within:ring-purple-500 transition-all">
                    <textarea
                        bind:value={query}
                        rows="3"
                        class="block w-full resize-none border-0 bg-transparent py-4 pl-4 pr-12 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-lg sm:leading-relaxed"
                        placeholder="e.g., Who is closest to going over budget? Which tasks are at risk this week?"
                    ></textarea>
                    <div class="absolute bottom-3 right-3">
                        <button
                            type="submit"
                            disabled={isQuerying || !query.trim()}
                            class="inline-flex items-center justify-center rounded-xl bg-purple-600 p-2 text-white hover:bg-purple-500 disabled:opacity-50 transition-colors"
                        >
                            {#if isQuerying}
                                <svg class="h-5 w-5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            {:else}
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
                                </svg>
                            {/if}
                        </button>
                    </div>
                </div>
            </form>

            {#if chatResponse}
                <div class="mt-8 flex gap-4">
                    <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-purple-100 text-purple-600">
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    </div>
                    <div class="pt-1.5">
                        <p class="text-lg leading-relaxed text-gray-800">{chatResponse}</p>
                    </div>
                </div>
            {/if}
        </div>

    </div>
</div>
